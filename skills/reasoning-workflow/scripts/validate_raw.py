#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,hashlib
from pathlib import Path
from semantic_core import validate_schema,finding

def load_records(path):
    x=json.loads(Path(path).read_text(encoding='utf-8')); return x if isinstance(x,list) else x.get('records',[])

def validate(records,root_dir=None,skill_root=None):
    skill_root=skill_root or Path(__file__).resolve().parents[1]; fs=[]; reg={}
    for r in records:
        fs+=validate_schema(r,skill_root/'schemas/raw-record.schema.json'); rid=r.get('raw_id')
        if rid in reg: fs.append(finding('ERROR','RAW_DUP_ID',f'duplicate raw_id {rid}',rid))
        reg[rid]=r
    adj={rid:list(r.get('derived_from',[]) or []) for rid,r in reg.items()}
    for rid,parents in adj.items():
        for p in parents:
            if p not in reg: fs.append(finding('ERROR','RAW_DANGLING_LINEAGE',f'{rid} derived_from missing {p}',rid,p))
    # cycle DFS
    color={k:0 for k in reg}; stack=[]
    def dfs(u):
        color[u]=1; stack.append(u)
        for v in adj.get(u,[]):
            if v not in reg: continue
            if color[v]==0: dfs(v)
            elif color[v]==1:
                i=stack.index(v); cyc=stack[i:]+[v]; fs.append(finding('ERROR','RAW_LINEAGE_CYCLE','raw lineage cycle: '+' -> '.join(cyc),*cyc))
        stack.pop(); color[u]=2
    for k in reg:
        if color[k]==0: dfs(k)
    if root_dir:
        root=Path(root_dir).resolve()
        for rid,r in reg.items():
            lp=r.get('local_path')
            if not lp: continue
            p=(root/lp).resolve()
            try:p.relative_to(root)
            except ValueError: fs.append(finding('ERROR','RAW_PATH_ESCAPE',f'{rid} local_path escapes root',rid)); continue
            if not p.exists(): fs.append(finding('ERROR','RAW_FILE_MISSING',f'{rid} local file missing: {lp}',rid)); continue
            h=r.get('content_hash'); alg=r.get('hash_algorithm')
            if h and alg:
                calc=hashlib.new(alg,p.read_bytes()).hexdigest()
                if calc.lower()!=h.lower(): fs.append(finding('ERROR','RAW_HASH_MISMATCH',f'{rid} {alg} mismatch',rid))
    return fs

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('raw_manifest'); ap.add_argument('--root'); ap.add_argument('--json',action='store_true'); a=ap.parse_args(); rec=load_records(a.raw_manifest); fs=validate(rec,a.root)
    if a.json: print(json.dumps({'findings':[f.as_dict() for f in fs]},indent=2))
    else:
        for f in fs: print(f'{f.severity} [{f.code}] {f.message}')
    return 1 if any(f.severity=='ERROR' for f in fs) else 0
if __name__=='__main__': raise SystemExit(main())
