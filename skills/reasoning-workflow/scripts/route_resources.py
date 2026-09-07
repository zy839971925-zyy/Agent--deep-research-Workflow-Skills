#!/usr/bin/env python3
import argparse,json
from pathlib import Path

def select(index,route,profile,gap_tags):
    if route.get('profile_version') != profile.get('profile_version'):
        raise ValueError('STALE_ROUTE')
    limit = route.get('reference_phase_limit', 2)
    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 0:
        raise ValueError('INVALID_REFERENCE_LIMIT')
    if limit == 0:
        return []
    allowed=set(route.get('required_families',[]))|set(route.get('optional_families',[])); tags=set(gap_tags or profile.get('active_gap_tags',[])); candidates=[]
    for e in index['references']:
        if e['family'] not in allowed: continue
        if profile.get('depth_class') not in e.get('typical_depth',[]): continue
        overlap=tags & set(e.get('load_when_tags',[]))
        if overlap: candidates.append((0,e['default_priority'],e,sorted(overlap)))
    # Light tasks with no unresolved structured gap need no reference beyond the root map.
    if not candidates and profile.get('depth_class')=='light' and not tags:
        return []
    # Otherwise load only one family entry per active family as a staged starting point, never bulk load.
    if not candidates:
        for fam in route.get('required_families',[]):
            fam_items=[e for e in index['references'] if e['family']==fam and profile.get('depth_class') in e.get('typical_depth',[])]
            if fam_items:
                e=sorted(fam_items,key=lambda x:x['default_priority'])[0]; candidates.append((1,e['default_priority'],e,[]))
    candidates.sort(key=lambda x:(x[0],x[1],x[2]['id']))
    out=[]; seen=set()
    for _,_,e,overlap in candidates:
        if e['id'] in seen: continue
        seen.add(e['id']); out.append({'reference_id':e['id'],'family':e['family'],'path':e['path'],'load_reason':'gap_match' if overlap else 'family_entry','current_gap':','.join(overlap) if overlap else 'family_entry','profile_version':profile['profile_version'],'context_cost_class':e['context_cost_class']})
        if len(out)>=limit: break
    return out

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('profile'); ap.add_argument('route'); ap.add_argument('--index',default='routing-index.json'); ap.add_argument('--gap-tag',action='append',default=[]); a=ap.parse_args()
    profile=json.loads(Path(a.profile).read_text()); route=json.loads(Path(a.route).read_text()); index=json.loads(Path(a.index).read_text())
    if route.get('profile_version')!=profile.get('profile_version'): print(json.dumps({'passed':False,'code':'STALE_ROUTE'},indent=2)); return 1
    selected=select(index,route,profile,a.gap_tag); print(json.dumps({'passed':True,'selected_references':selected},indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
