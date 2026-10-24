#!/usr/bin/env python3
"""Normalize and prepare references in one step; never executes the task or tools."""
from pathlib import Path
import argparse,json
from routing_core import validate_profile,recheck_profile,route_task
from route_resources import select
ROOT=Path(__file__).resolve().parents[1]

def prepare(profile,signals=(),gap_tags=(),root=ROOT):
    errors=validate_profile(profile,root)
    if errors:
        return {'passed':False,'status':'invalid_profile','errors':errors,'task_executed':False}
    profile=recheck_profile(profile,signals)
    route=route_task(profile)
    try:
        index=json.loads((root/'routing-index.json').read_text())
        selected=select(index,route,profile,gap_tags)
        for ref in selected:
            path=(root/ref['path']).resolve()
            path.relative_to(root.resolve())
            if not path.is_file():raise ValueError('REQUIRED_RESOURCE_UNAVAILABLE: '+ref['reference_id'])
        ids={x['reference_id'] for x in selected};tags=set(gap_tags or profile.get('active_gap_tags',[]))
        allowed=set(route['required_families'])|set(route['optional_families'])
        deferred=[{'reference_id':x['id'],'path':x['path'],'reason':'matching_gap_next_phase'} for x in index['references']
            if x['id'] not in ids and x['family'] in allowed and tags&set(x.get('load_when_tags',[]))]
    except (ValueError,KeyError,TypeError,OSError) as exc:
        return {'passed':False,'status':'blocked','task_profile':profile,'route':route,'errors':[str(exc)],
            'next_action':'Restore required resources or disclose an explicit capability-limited result; do not claim full requested-depth execution.', 'task_executed':False}
    return {'passed':True,'status':'prepared','task_profile':profile,'route':route,
        'selected_references':selected,'deferred_references':deferred,'task_executed':False,
        'authority_granted':False}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('profile');p.add_argument('--signal',action='append',default=[]);p.add_argument('--gap-tag',action='append',default=[]);a=p.parse_args()
    try:result=prepare(json.loads(Path(a.profile).read_text()),a.signal,a.gap_tag)
    except (ValueError,TypeError,OSError) as e:result={'passed':False,'status':'invalid_input','errors':[str(e)],'task_executed':False}
    print(json.dumps(result,indent=2));return 0 if result['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
