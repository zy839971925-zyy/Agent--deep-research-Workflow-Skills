#!/usr/bin/env python3
import argparse,json
from pathlib import Path
from routing_core import validate_profile,route_task,recheck_profile

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('profile'); ap.add_argument('--root',default='.'); ap.add_argument('--signals',nargs='*',default=[]); a=ap.parse_args()
    p=json.loads(Path(a.profile).read_text()); errs=validate_profile(p,Path(a.root))
    if errs: print(json.dumps({'passed':False,'errors':errs},indent=2)); return 1
    if a.signals: p=recheck_profile(p,a.signals)
    print(json.dumps({'passed':True,'task_profile':p,'route':route_task(p)},indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
