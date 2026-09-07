#!/usr/bin/env python3
from pathlib import Path
import argparse,zipfile,tempfile,json,hashlib

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('portable');ap.add_argument('modular');a=ap.parse_args();errs=[]
    with tempfile.TemporaryDirectory() as td:
        td=Path(td)
        with zipfile.ZipFile(a.portable) as z:z.extractall(td/'p')
        with zipfile.ZipFile(a.modular) as z:z.extractall(td/'m')
        proot=td/'p'/'reasoning-workflow';mroot=td/'m'/'reasoning-workflow-modular';manifest=json.loads((proot/'SEMANTIC_MANIFEST.json').read_text())['canonical_hashes']
        for rel,h in manifest.items():
            pp=proot/rel
            if not pp.is_file() or sha(pp)!=h:errs.append(f'portable semantic mismatch {rel}')
        for skill in (mroot/'skills').iterdir():
            for rel,h in manifest.items():
                p=skill/rel
                if not p.is_file() or sha(p)!=h:errs.append(f'{skill.name} semantic mismatch {rel}')
    if errs:[print('ERROR:',e) for e in errs];return 1
    print('OK: portable/modular shared semantic hashes are consistent');return 0
if __name__=='__main__':raise SystemExit(main())
