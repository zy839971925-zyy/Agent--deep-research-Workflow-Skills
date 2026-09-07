#!/usr/bin/env python3
from pathlib import Path
import argparse,json
from learning_core import retrieve

def main():
    ap=argparse.ArgumentParser();ap.add_argument('records');ap.add_argument('--task-tag',action='append',default=[]);ap.add_argument('--gap-tag',action='append',default=[]);ap.add_argument('--limit',type=int,default=3);a=ap.parse_args();r=json.loads(Path(a.records).read_text());items=r if isinstance(r,list) else r.get('learnings',[]);print(json.dumps({'selected':retrieve(items,a.task_tag,a.gap_tag,a.limit)},indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
