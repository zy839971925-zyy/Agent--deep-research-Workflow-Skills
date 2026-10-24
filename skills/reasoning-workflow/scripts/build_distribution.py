#!/usr/bin/env python3
"""Build a reproducible, versioned Portable ZIP and update source/distribution checksums."""
from pathlib import Path
import hashlib, json, stat, zipfile
ROOT=Path(__file__).resolve().parents[3]
PACKAGE=ROOT/'skills/reasoning-workflow'
DIST=ROOT/'dist'
def sha(data):return hashlib.sha256(data).hexdigest()
def package_files(include_sum=False):
 return sorted(p for p in PACKAGE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc' and (include_sum or p.name!='SHA256SUMS'))
def main():
 meta=json.loads((PACKAGE/'RELEASE.json').read_text(encoding='utf-8'));version=meta['version']
 checks=''.join(f"{sha(p.read_bytes())}  {p.relative_to(PACKAGE).as_posix()}\n" for p in package_files())
 (PACKAGE/'SHA256SUMS').write_text(checks,encoding='utf-8')
 DIST.mkdir(exist_ok=True);target=DIST/f'reasoning-workflow-{version}.zip'
 with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_STORED) as z:
  for p in package_files(include_sum=True):
   name='reasoning-workflow/'+p.relative_to(PACKAGE).as_posix()
   info=zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0));info.compress_type=zipfile.ZIP_STORED;info.create_system=3
   mode=0o755 if p.stat().st_mode & stat.S_IXUSR else 0o644;info.external_attr=((stat.S_IFREG|mode) & 0xffff)<<16
   z.writestr(info,p.read_bytes())
 archives=sorted(DIST.glob('reasoning-workflow-*.zip'))
 sums=''.join(f"{sha(p.read_bytes())}  {p.name}\n" for p in archives)
 (DIST/'SHA256SUMS').write_text(sums,encoding='utf-8')
 print(json.dumps({'version':version,'archive':str(target.relative_to(ROOT)),'sha256':sha(target.read_bytes()),'source_files':len(package_files(include_sum=True)),'package_checksum_entries':len(package_files()),'distribution_archives':len(archives)},indent=2))
if __name__=='__main__':main()
