#!/usr/bin/env python3
from pathlib import Path
import argparse,json
try: import jsonschema
except ImportError: jsonschema=None
from learning_core import validate_learning_semantics

def main():
    ap=argparse.ArgumentParser();ap.add_argument('record');ap.add_argument('--root',default='.');a=ap.parse_args();d=json.loads(Path(a.record).read_text());fs=[]
    if jsonschema is None: fs.append({'severity':'ERROR','code':'JSONSCHEMA_MISSING'})
    else:
        s=json.loads((Path(a.root)/'schemas'/'learning-record.schema.json').read_text())
        for e in jsonschema.Draft202012Validator(s).iter_errors(d):fs.append({'severity':'ERROR','code':'SCHEMA','message':e.message})
    fs+=validate_learning_semantics(d);print(json.dumps({'passed':not fs,'findings':fs},indent=2));return 1 if fs else 0
if __name__=='__main__':raise SystemExit(main())
