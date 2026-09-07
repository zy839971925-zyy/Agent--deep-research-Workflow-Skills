#!/usr/bin/env python3
from pathlib import Path
import argparse,json,importlib.util
try:import jsonschema
except ImportError:jsonschema=None

def main():
    ap=argparse.ArgumentParser();ap.add_argument('root',nargs='?',default='.');a=ap.parse_args();root=Path(a.root);errs=[]
    if jsonschema is None:errs.append('jsonschema missing')
    for p in sorted((root/'schemas').glob('*.schema.json')):
        try:jsonschema.Draft202012Validator.check_schema(json.loads(p.read_text()))
        except Exception as e:errs.append(f'{p.name}: {e}')
    try:
        idx=json.loads((root/'routing-index.json').read_text());
        for e in idx['references']:
            for k in ('id','family','path','load_when','do_not_load_when','prerequisites','consumes','produces','return_to','typical_depth','machine_enforced','context_cost_class'):
                if k not in e:errs.append(f"routing {e.get('id')} missing {k}")
    except Exception as e:errs.append(f'routing-index: {e}')
    if errs:
        [print('ERROR:',x) for x in errs];return 1
    print('OK: workflow schemas and routing metadata passed');return 0
if __name__=='__main__':raise SystemExit(main())
