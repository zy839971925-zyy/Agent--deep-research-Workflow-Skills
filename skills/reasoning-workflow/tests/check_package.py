#!/usr/bin/env python3
"""Read-only portable package checks. Optional --output writes the observed receipt."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import argparse,ast,json,sys
ROOT=Path(__file__).resolve().parents[1]
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set()
 def handle_starttag(self,tag,attrs):
  attrs=dict(attrs)
  if tag=='a' and attrs.get('href'):self.links.append(attrs['href'])
  if attrs.get('id'):self.ids.add(attrs['id'])
def check(root):
 import markdown,jsonschema
 failures=[];markdowns={};count=0;anchors=0;python_count=0;json_count=0;schema_count=0
 for path in sorted(root.rglob('*.md')):
  parser=Links();parser.feed(markdown.markdown(path.read_text(),extensions=['fenced_code','tables','toc']));markdowns[path.resolve()]=parser
 for path,parser in markdowns.items():
  for href in parser.links:
   u=urlsplit(href)
   if u.scheme or u.netloc:continue
   count+=1;target=(path.parent/unquote(u.path)).resolve() if u.path else path
   if not target.exists():failures.append({'kind':'missing_link_target','file':str(path.relative_to(root)),'href':href});continue
   if u.fragment and target.suffix=='.md':
    anchors+=1
    if unquote(u.fragment) not in markdowns[target].ids:failures.append({'kind':'missing_link_anchor','file':str(path.relative_to(root)),'href':href})
 for path in sorted(root.rglob('*.py')):
  python_count+=1
  try:ast.parse(path.read_text(),filename=str(path))
  except Exception as e:failures.append({'kind':'python_ast','file':str(path.relative_to(root)),'error':str(e)})
 for path in sorted(root.rglob('*.json')):
  json_count+=1
  try:
   value=json.loads(path.read_text())
   if path.name.endswith('.schema.json'):schema_count+=1;jsonschema.Draft202012Validator.check_schema(value)
  except Exception as e:failures.append({'kind':'json_or_schema','file':str(path.relative_to(root)),'error':str(e)})
 index=json.loads((root/'routing-index.json').read_text());seen=set()
 for entry in index['references']:
  if entry['id'] in seen:failures.append({'kind':'duplicate_reference_id','id':entry['id']})
  seen.add(entry['id']);target=(root/entry['path']).resolve()
  if not target.is_relative_to(root) or not target.is_file():failures.append({'kind':'invalid_reference_path','id':entry['id']})
 entry=(root/'SKILL.md').read_text();meta=json.loads((root/'RELEASE.json').read_text())
 if meta['version'] not in entry or meta['model_entry']!='SKILL.md':failures.append({'kind':'release_entry_mismatch'})
 return {'release_version':meta['version'],'passed':not failures,'markdown_files_checked':len(markdowns),'local_markdown_links_checked':count,'local_markdown_anchors_checked':anchors,'python_ast_checked':python_count,'json_parsed':json_count,'json_schemas_checked':schema_count,'routing_reference_paths_checked':len(index['references']),'failures':failures,'note':'Static package structure only; not model compliance, dependency installation or external execution.'}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path);a=p.parse_args();result=check(ROOT)
 if a.output:a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(result,ensure_ascii=False,indent=2));return 0 if result['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
