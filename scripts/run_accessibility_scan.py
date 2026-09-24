"""Run local axe with project-local Playwright; no install, CDN, server start, or auth bypass."""
from __future__ import annotations
import argparse,json,re,subprocess,sys
from pathlib import Path
from run_browser_execution import ROOT, VIEWPORTS, SESSION_RE, atomic, detector, request

HELPER=r'''const fs=require('fs'),path=require('path');const i=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));let pw,axePlay,axe;
try{pw=require('playwright')}catch(e){try{pw=require('@playwright/test')}catch(_){process.exit(2)}}
try{axePlay=require('@axe-core/playwright')}catch(_){};try{axe=require('axe-core')}catch(_){}
(async()=>{let b;const out={scans:[],errors:[]};try{b=await pw.chromium.launch({headless:true});for(const r of i.routes)for(const v of i.viewports){let c,p,file=`${r.safe_id}__${v.id}__iter-${String(i.iteration).padStart(2,'0')}__axe.json`;try{c=await b.newContext({viewport:{width:v.width,height:v.height}});p=await c.newPage();await p.goto(new URL(r.route,i.base_url).href,{waitUntil:'domcontentloaded',timeout:i.timeout_ms});let result;if(axePlay){let q=new axePlay.AxeBuilder({page:p});for(const x of i.include)q.include(x);for(const x of i.exclude)q.exclude(x);result=await q.analyze()}else if(axe){await p.evaluate(axe.source);result=await p.evaluate(async o=>await axe.run(o),{runOnly:i.include.length?{type:'rule',values:i.include}:undefined,rules:Object.fromEntries(i.exclude.map(x=>[x,{enabled:false}]))})}else throw Error('AXE_NOT_AVAILABLE');fs.writeFileSync(path.join(i.out,file),JSON.stringify({schema_version:1,page_id:r.page_id,route:r.route,viewport:v.id,iteration:i.iteration,results:result}));out.scans.push({id:`${r.page_id}:${v.id}:${i.iteration}`,page_id:r.page_id,route:r.route,viewport:v.id,width:v.width,height:v.height,iteration:i.iteration,status:'SCANNED',file,violations:result.violations.length,incomplete:result.incomplete.length})}catch(e){out.errors.push({code:String(e.message||e).includes('AXE_NOT')?'AXE_NOT_AVAILABLE':'ACCESSIBILITY_SCAN_FAILURE',page_id:r.page_id,route:r.route,viewport:v.id,message:String(e.message||e).slice(0,500)});out.scans.push({id:`${r.page_id}:${v.id}:${i.iteration}`,page_id:r.page_id,route:r.route,viewport:v.id,width:v.width,height:v.height,iteration:i.iteration,status:'SCAN_FAILURE',file:null,violations:0,incomplete:0})}finally{if(c)await c.close().catch(()=>{})}}}catch(e){out.errors.push({code:'AXE_RUNTIME_FAILURE',message:String(e.message||e).slice(0,500)})}finally{if(b)await b.close().catch(()=>{});console.log(JSON.stringify(out))}})();'''
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--project',default='.');ap.add_argument('--dry-run',action='store_true');a=ap.parse_args();project=Path(a.project).resolve()
 try:
  raw=json.loads(Path(a.input).read_text(encoding='utf8'));sid=raw['session_id'];base=raw['base_url'];routes=raw['routes'];views=raw.get('viewports',['desktop','mobile']);it=raw.get('iteration',1)
  if not SESSION_RE.fullmatch(sid) or not isinstance(routes,list) or not routes or any(v not in VIEWPORTS for v in views) or it<1:raise ValueError('invalid accessibility input')
 except Exception as e: print(json.dumps({'status':'INVALID_INPUT','error':str(e)}));return 3
 cap=detector(project);ax=cap['accessibility'];available=cap['playwright']['package_present']['status']=='AVAILABLE' and (ax['axe_playwright']['status']=='AVAILABLE' or ax['axe_core']['status']=='AVAILABLE')
 output=Path(raw.get('output_dir','.evidence'));output=output if output.is_absolute() else project/output
 try: output.resolve().relative_to(project)
 except ValueError: print(json.dumps({'status':'INVALID_INPUT','error':'output_dir must remain inside project root'}));return 3
 session=output/sid;plan={'status':'DRY_RUN','strategy':ax['strategy'] if available else 'BLOCKED','session_id':sid,'routes':[r.get('route') for r in routes],'viewports':views,'capability':ax}
 if a.dry_run:print(json.dumps(plan));return 0
 out=session/'accessibility';out.mkdir(parents=True,exist_ok=True)
 if not available or not request(base):
  status='BLOCKED';manifest={'schema_version':1,'session_id':sid,'iteration':it,'status':status,'scans':[],'errors':[{'code':'AXE_NOT_AVAILABLE' if not available else 'READINESS_TIMEOUT'}]};atomic(out/'accessibility-manifest.json',manifest);print(json.dumps({'status':status,'manifest':str(out/'accessibility-manifest.json')}));return 2
 helper=out/'axe-helper.cjs';payload=out/'axe-input.json';
 try:
  helper.write_text(HELPER,encoding='utf8');data={'base_url':base,'routes':[{**r,'safe_id':re.sub(r'[^A-Za-z0-9_-]','-',r['page_id'])} for r in routes],'viewports':[{'id':v,**VIEWPORTS[v]} for v in views],'iteration':it,'out':str(out),'include':raw.get('rules',{}).get('include',[]),'exclude':raw.get('rules',{}).get('exclude',[]),'timeout_ms':raw.get('timeout_ms',30000)};atomic(payload,data);run=subprocess.run(['node',str(helper),str(payload)],cwd=project,capture_output=True,text=True,timeout=120);res=json.loads(run.stdout);done=sum(x['status']=='SCANNED' for x in res['scans']);status='COMPLETED' if done==len(routes)*len(views) else 'PARTIAL' if done else 'FAILED';atomic(out/'accessibility-manifest.json',{'schema_version':1,'session_id':sid,'iteration':it,'status':status,'scans':res['scans'],'errors':res['errors']});print(json.dumps({'status':status,'manifest':str(out/'accessibility-manifest.json')}));return 0 if status=='COMPLETED' else 4
 finally:
  helper.unlink(missing_ok=True);payload.unlink(missing_ok=True)
if __name__=='__main__':raise SystemExit(main())
