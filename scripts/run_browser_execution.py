"""Playwright runtime orchestrator. Uses only project-local Playwright; never installs tools."""
from __future__ import annotations

import argparse, json, os, re, signal, subprocess, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VIEWPORTS = json.loads((ROOT / "execution/viewports.json").read_text(encoding="utf-8"))
SESSION_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")

HELPER = r'''const fs=require('fs'),path=require('path');
const i=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));let pw;
try{pw=require('playwright')}catch(e){try{pw=require('@playwright/test')}catch(e2){console.error('PLAYWRIGHT_IMPORT_FAILURE');process.exit(2)}}
(async()=>{const out={captures:[],errors:[],console:[]};let browser;
 try{browser=await pw[i.browser].launch({headless:true});
  for(const r of i.routes) for(const v of i.viewports){let c,p,id=`${r.page_id}:${v.id}:${i.iteration}`,file=`pages/${r.safe_id}__${v.id}__iter-${String(i.iteration).padStart(2,'0')}.png`;
   try{c=await browser.newContext({viewport:{width:v.width,height:v.height}});p=await c.newPage();
    if(i.collect_console){p.on('console',m=>{if(m.type()==='error')out.console.push({page_id:r.page_id,viewport:v.id,message:m.text()})});p.on('pageerror',e=>out.console.push({page_id:r.page_id,viewport:v.id,message:String(e.message||e)}))}
    await p.goto(new URL(r.route,i.base_url).href,{waitUntil:'domcontentloaded',timeout:i.navigation_timeout_ms});
    const basic=await p.evaluate(()=>({body:!!document.body,text:(document.body?.innerText||'').trim().length,root:!!document.querySelector('main,[role="main"],#root,#app')}));
    if(!basic.body||!basic.text)throw Object.assign(new Error('blank render'),{code:'BLANK_RENDER'});
    if(r.expected_selector && !await p.locator(r.expected_selector).count())throw Object.assign(new Error('expected selector missing'),{code:'NAVIGATION_FAILURE'});
    if(r.expected_text && !await p.getByText(r.expected_text,{exact:false}).count())throw Object.assign(new Error('expected text missing'),{code:'NAVIGATION_FAILURE'});
    await p.screenshot({path:path.join(i.output_dir,file),fullPage:i.full_page,timeout:i.screenshot_timeout_ms});
    out.captures.push({id,page_id:r.page_id,route:r.route,viewport:v.id,width:v.width,height:v.height,iteration:i.iteration,status:'CAPTURED',file,basic_render:basic});
   }catch(e){out.errors.push({code:e.code||'SCREENSHOT_FAILURE',page_id:r.page_id,route:r.route,viewport:v.id,message:String(e.message||e).slice(0,500),recoverable:true});out.captures.push({id,page_id:r.page_id,route:r.route,viewport:v.id,width:v.width,height:v.height,iteration:i.iteration,status:'SCREENSHOT_FAILURE',file:null})}
   finally{if(c)await c.close().catch(()=>{})}
  }
 }catch(e){out.errors.push({code:'BROWSER_LAUNCH_FAILURE',page_id:null,route:null,viewport:null,message:String(e.message||e).slice(0,500),recoverable:false})}
 finally{if(browser)await browser.close().catch(()=>{});console.log(JSON.stringify(out))}
})();'''

def atomic(path: Path, data: object) -> None:
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(temp, path)

def err(code: str, message: str, **extra: object) -> dict[str, object]:
    return {"code": code, "page_id": extra.get("page_id"), "route": extra.get("route"), "viewport": extra.get("viewport"), "message": message[:500], "recoverable": bool(extra.get("recoverable", False))}

def inside(root: Path, candidate: Path) -> Path:
    resolved = candidate.resolve()
    try: resolved.relative_to(root.resolve())
    except ValueError: raise ValueError("output_dir must remain inside project root")
    return resolved

def request(url: str) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=2) as response: return response.status < 500
    except Exception: return False

def ready(url: str, timeout_ms: int) -> bool:
    end = time.monotonic() + timeout_ms / 1000
    while time.monotonic() < end:
        if request(url): return True
        time.sleep(.5)
    return False

def detector(project: Path) -> dict[str, object]:
    run = subprocess.run([sys.executable, str(ROOT / "scripts/detect_capabilities.py"), str(project)], capture_output=True, text=True, timeout=10)
    if run.returncode: raise RuntimeError("capability detector failed")
    return json.loads(run.stdout)

def validate(raw: object, project: Path) -> tuple[dict[str, object], Path]:
    if not isinstance(raw, dict): raise ValueError("input must be an object")
    sid, base, routes, names, iteration = raw.get("session_id"), raw.get("base_url"), raw.get("routes"), raw.get("viewports"), raw.get("iteration", 1)
    if not isinstance(sid, str) or not SESSION_RE.fullmatch(sid): raise ValueError("invalid session_id")
    if not isinstance(base, str) or not re.match(r"^https?://[^/]+", base): raise ValueError("invalid base_url")
    if not isinstance(routes, list) or not routes: raise ValueError("routes must be non-empty")
    if not isinstance(names, list) or not names or any(v not in VIEWPORTS for v in names): raise ValueError("unknown viewport ID")
    if not isinstance(iteration, int) or iteration < 1: raise ValueError("iteration must be >= 1")
    for route in routes:
        if not isinstance(route, dict) or not isinstance(route.get("page_id"), str) or not isinstance(route.get("route"), str) or not route["route"].startswith("/"):
            raise ValueError("each route needs page_id and absolute route")
    output = Path(raw.get("output_dir", project / ".evidence"))
    output = inside(project, output if output.is_absolute() else project / output)
    return raw, output / sid

def stop(process: subprocess.Popen[str] | None, timeout_ms: int) -> bool:
    if not process or process.poll() is not None: return True
    process.terminate()
    try: process.wait(timeout=timeout_ms / 1000); return True
    except subprocess.TimeoutExpired:
        process.kill(); process.wait(timeout=timeout_ms / 1000); return False

def main() -> int:
    ap=argparse.ArgumentParser(description="Run existing project-local Playwright visual capture")
    ap.add_argument("--input", required=True); ap.add_argument("--project", default="."); ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--allow-start", action="store_true"); ap.add_argument("--debug", action="store_true")
    args=ap.parse_args(); project=Path(args.project).resolve()
    try: raw, session=validate(json.loads(Path(args.input).read_text(encoding="utf-8")), project)
    except (OSError,json.JSONDecodeError,ValueError) as exc:
        print(json.dumps({"status":"INVALID_INPUT","error":str(exc)})); return 3
    cap=detector(project); pw=cap["playwright"]["package_present"]["status"] == "AVAILABLE"; node=cap["runtime"]["node"]["status"] == "AVAILABLE"
    plan={"status":"DRY_RUN","strategy":"playwright" if pw and node else "BLOCKED","session_id":raw["session_id"],"output_dir":str(session),"routes":[r["route"] for r in raw["routes"]],"viewports":raw["viewports"],"capability":cap["playwright"]}
    if args.dry_run: print(json.dumps(plan)); return 0
    session.mkdir(parents=True,exist_ok=True); (session/"pages").mkdir(exist_ok=True); (session/"logs").mkdir(exist_ok=True)
    report={"schema_version":1,"session_id":raw["session_id"],"strategy":"playwright","base_url":raw["base_url"],"iteration":raw["iteration"],"status":"BLOCKED","routes_total":len(raw["routes"]),"captures_expected":len(raw["routes"])*len(raw["viewports"]),"captures_completed":0,"errors":[],"server_owned":False,"readiness":None,"cleanup":{"browser_closed":False,"server_stopped":False,"temporary_files_removed":False}}
    if not pw or not node:
        report["errors"].append(err("PLAYWRIGHT_IMPORT_FAILURE","project-local Playwright or Node unavailable")); atomic(session/"execution-report.json",report); atomic(session/"manifest.json",{**report,"captures":[]}); print(json.dumps({"status":"BLOCKED","report":str(session/"execution-report.json")})); return 2
    process=None; captures=[]; helper=None; payload=None
    try:
        if not request(raw["base_url"]):
            start=raw.get("start",{}); command=start.get("command") if isinstance(start,dict) else None
            if not args.allow_start or not isinstance(command,list) or not command or not all(isinstance(x,str) and x for x in command): raise RuntimeError("SERVER_START_FAILURE: no explicit --allow-start argv command")
            process=subprocess.Popen(command,cwd=project,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,text=True); report["server_owned"]=True
        timeout=int(raw.get("readiness",{}).get("timeout_ms",60000)); report["readiness"]={"url":raw["base_url"],"timeout_ms":timeout}
        if not ready(raw["base_url"],timeout): raise RuntimeError("READINESS_TIMEOUT")
        helper=session/"runtime-helper.cjs"; payload=session/"runtime-input.json"; helper.write_text(HELPER,encoding="utf-8")
        opts=raw.get("options",{}) if isinstance(raw.get("options",{}),dict) else {}
        payload_data={"base_url":raw["base_url"],"routes":[{**r,"safe_id":re.sub(r"[^A-Za-z0-9_-]","-",r["page_id"])} for r in raw["routes"]],"viewports":[{"id":v,**VIEWPORTS[v]} for v in raw["viewports"]],"iteration":raw["iteration"],"output_dir":str(session),"browser":opts.get("browser","chromium"),"collect_console":bool(opts.get("collect_console",False)),"full_page":bool(opts.get("full_page",True)),"navigation_timeout_ms":int(opts.get("navigation_timeout_ms",30000)),"screenshot_timeout_ms":int(opts.get("screenshot_timeout_ms",30000))}
        atomic(payload,payload_data); run=subprocess.run(["node",str(helper),str(payload)],cwd=project,capture_output=True,text=True,timeout=max(60,payload_data["navigation_timeout_ms"]//1000*len(raw["routes"])*len(raw["viewports"])+30))
        result=json.loads(run.stdout) if run.stdout.strip() else {"captures":[],"errors":[err("BROWSER_LAUNCH_FAILURE",run.stderr or "helper produced no output")]}
        report["errors"].extend(result.get("errors",[])); captures=result.get("captures",[]); report["captures_completed"]=sum(c.get("status")=="CAPTURED" for c in captures)
        if result.get("console"): atomic(session/"logs/console.json",{"schema_version":1,"events":result["console"]})
        report["status"]="COMPLETED" if report["captures_completed"]==report["captures_expected"] else "PARTIAL" if report["captures_completed"] else "FAILED"
        if report["status"]=="PARTIAL": report["errors"].append(err("PARTIAL_EXECUTION","some requested captures failed",recoverable=True))
        manifest={"schema_version":1,"session_id":raw["session_id"],"strategy":"playwright","base_url":raw["base_url"],"iteration":raw["iteration"],"status":report["status"],"captures":captures}
        atomic(session/"manifest.json",manifest)
    except Exception as exc:
        code=str(exc).split(":",1)[0] if re.match(r"^[A-Z_]+",str(exc)) else "RUNTIME_RUNNER_FAILURE"; report["errors"].append(err(code,str(exc))); report["status"]="PARTIAL" if captures else ("FAILED" if code not in {"SERVER_START_FAILURE","READINESS_TIMEOUT"} else "BLOCKED"); atomic(session/"manifest.json",{**report,"captures":captures})
    finally:
        removed=True
        for temporary in (helper,payload):
            if temporary:
                try: temporary.unlink(missing_ok=True)
                except OSError: removed=False
        report["cleanup"]["temporary_files_removed"]=removed
        report["cleanup"]["server_stopped"]=stop(process,int(raw.get("cleanup_timeout_ms",5000))) if report["server_owned"] else False; report["cleanup"]["browser_closed"]=True; atomic(session/"execution-report.json",report)
    print(json.dumps({"status":report["status"],"report":str(session/"execution-report.json"),"manifest":str(session/"manifest.json")})); return {"COMPLETED":0,"PARTIAL":4,"BLOCKED":2}.get(report["status"],1)

if __name__=="__main__":
    raise SystemExit(main())
