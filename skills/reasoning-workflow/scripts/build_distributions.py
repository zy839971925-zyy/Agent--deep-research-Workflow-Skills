#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse,shutil,json,hashlib,zipfile,tempfile

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def zipdir(src,out):
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(src.rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc':
                info = zipfile.ZipInfo(p.relative_to(src.parent).as_posix(), (1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(info, p.read_bytes())

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',default='.');ap.add_argument('--out-dir',default='.');a=ap.parse_args();src=Path(a.source).resolve();out=Path(a.out_dir).resolve();out.mkdir(parents=True,exist_ok=True)
    idx=json.loads((src/'routing-index.json').read_text()); shared=[p for sub in ('schemas','scripts') for p in sorted((src/sub).glob('*')) if p.is_file() and p.suffix!='.pyc']+[src/'routing-index.json']
    manifest={'canonical_hashes':{str(p.relative_to(src)):sha(p) for p in shared}}
    (src/'SEMANTIC_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    with tempfile.TemporaryDirectory() as td:
        td=Path(td)
        # portable
        proot=td/'portable'/'reasoning-workflow';shutil.copytree(src,proot,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        (proot/'SEMANTIC_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
        pzip=out/'reasoning-workflow-portable.zip';zipdir(proot,pzip)
        # modular
        mbase=td/'modular'/'reasoning-workflow-modular';skills=mbase/'skills';skills.mkdir(parents=True)
        (mbase/'SEMANTIC_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
        (mbase/'README.md').write_text('# Reasoning Workflow Modular\n\nGenerated from the same canonical source as the portable package. Six family Skills share machine semantics by hash.\n')
        names={'core-reasoning':'reasoning-core','deep-research':'deep-research','decision-analysis':'decision-analysis','execution-control':'execution-control','audit-verification':'audit-verification','workflow-learning':'workflow-learning'}
        for fam,skillname in names.items():
            d=skills/skillname;d.mkdir();(d/'references').mkdir();(d/'families').mkdir()
            desc=next(f['description'] for f in idx['families'] if f['id']==fam)
            (d/'SKILL.md').write_text(f"---\nname: {skillname}\ndescription: {desc}\n---\n\n# {skillname}\n\nThis is a generated Reasoning Workflow Skill Family. Use the family index and progressive router; do not bulk-load references.\n\n[Family index](families/{fam}.md)\n")
            # Vendor the shared reference/family tree for runtimes that require every Skill directory to be self-contained.
            # The active family index + routing-index still controls what enters model context; presence on disk is not a load instruction.
            shutil.rmtree(d/'references'); shutil.copytree(src/'references',d/'references')
            shutil.rmtree(d/'families'); shutil.copytree(src/'families',d/'families')
            for sub in ('schemas','scripts'):
                shutil.copytree(src/sub,d/sub,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
            shutil.copy2(src/'routing-index.json',d/'routing-index.json');(d/'SEMANTIC_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
        mzip=out/'reasoning-workflow-modular.zip';zipdir(mbase,mzip)
    print(json.dumps({'portable':str(pzip),'modular':str(mzip),'manifest':manifest},indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
