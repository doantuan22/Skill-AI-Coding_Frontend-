"""Validate accessibility manifest and scan evidence structure; no axe execution."""
from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];VP=json.loads((ROOT/'execution/viewports.json').read_text())
def main():
 if len(sys.argv)!=2:return 3
 root=Path(sys.argv[1]);m=json.loads((root/'accessibility-manifest.json').read_text());errs=[];seen=set()
 if m.get('schema_version')!=1:errs+=['schema']
 for s in m.get('scans',[]):
  if not s.get('id') or s['id'] in seen:errs+=['duplicate scan']
  seen.add(s.get('id'));v=VP.get(s.get('viewport'),{})
  if s.get('width')!=v.get('width') or s.get('height')!=v.get('height'):errs+=['viewport']
  if s.get('status')=='SCANNED':
   p=root/s.get('file','');
   if not p.is_file():errs+=['missing scan file'];continue
   d=json.loads(p.read_text());r=d.get('results',{})
   if d.get('schema_version')!=1 or not isinstance(r.get('violations',[]),list) or s.get('violations')!=len(r.get('violations',[])):errs+=['count/schema']
 if errs:print('Accessibility evidence invalid: '+', '.join(errs));return 1
 print(json.dumps({'status':'VALID','scans':len(m.get('scans',[]))}));return 0
if __name__=='__main__':raise SystemExit(main())
