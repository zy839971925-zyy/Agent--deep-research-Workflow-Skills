#!/usr/bin/env python3
import argparse,json
from pathlib import Path
from routing_core import validate_profile,route_task,recheck_profile

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('profile'); ap.add_argument('--root',default=str(Path(__file__).resolve().parents[1])); ap.add_argument('--index'); ap.add_argument('--signals',nargs='*',default=[]); a=ap.parse_args()
    p=json.loads(Path(a.profile).read_text()); errs=validate_profile(p,Path(a.root))
    if errs: print(json.dumps({'passed':False,'errors':errs},indent=2)); return 1
    known=set(json.loads((Path(a.root)/'schemas/task-profile.schema.json').read_text())['properties']['recheck_triggers']['items']['enum'])
    if set(a.signals)-known:
        print(json.dumps({'passed':False,'errors':['UNKNOWN_SIGNAL']})); return 1
    p=recheck_profile(p,a.signals)
    errs=validate_profile(p,Path(a.root))
    if errs: print(json.dumps({'passed':False,'errors':errs})); return 1
    print(json.dumps({'passed':True,'task_profile':p,'route':route_task(p,json.loads(Path(a.index).read_text()) if a.index else None)},indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
