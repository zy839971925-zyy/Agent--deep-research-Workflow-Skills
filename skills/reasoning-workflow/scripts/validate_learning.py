#!/usr/bin/env python3
from pathlib import Path
import argparse,json
from learning_core import admit_record,file_evidence_resolver

def main():
    ap=argparse.ArgumentParser();ap.add_argument('record');ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--validation-evidence',type=Path);a=ap.parse_args()
    try:fs=admit_record(json.loads(Path(a.record).read_text()),a.root,file_evidence_resolver(a.validation_evidence))
    except (ValueError,OSError,TypeError) as e:fs=[{'severity':'ERROR','code':'LEARNING_INPUT','message':str(e)}]
    print(json.dumps({'passed':not fs,'findings':fs},indent=2));return 1 if fs else 0
if __name__=='__main__':raise SystemExit(main())
