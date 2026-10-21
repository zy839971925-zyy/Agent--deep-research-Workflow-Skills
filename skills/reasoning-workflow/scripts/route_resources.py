#!/usr/bin/env python3
import argparse,json
from pathlib import Path
from routing_core import recheck_profile,route_task,route_is_stale,compute_index_fingerprint

def select(index,route,profile,gap_tags):
    if recheck_profile(profile,[])!=profile: raise ValueError("PROFILE_RECHECK_REQUIRED")
    if route.get('profile_version') != profile.get('profile_version'):
        raise ValueError('STALE_ROUTE')
    if route_is_stale(route,profile,compute_index_fingerprint(index)): raise ValueError('STALE_ROUTE: ROUTE_REQUIREMENTS_MISMATCH')
    limit = route.get('reference_phase_limit', 2)
    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 0:
        raise ValueError('INVALID_REFERENCE_LIMIT')
    if limit == 0 and set(route.get('required_families',[])) <= {'core-reasoning'}:
        return []
    required=set(route.get('required_families',[]))
    allowed=required|set(route.get('optional_families',[])); tags=set(gap_tags or profile.get('active_gap_tags',[]))
    if profile.get('depth_class')=='light' and not tags and required <= {'core-reasoning'}: return []
    candidates=[]
    for e in index['references']:
        if e['family'] not in allowed and not (profile.get('depth_class')=='ultra' and e['id']=='ultra-research'): continue
        if e['family'] not in required and profile.get('depth_class') not in e.get('typical_depth',[]): continue
        overlap=tags & set(e.get('load_when_tags',[]))
        if overlap or e['family'] in required or (profile.get('depth_class')=='ultra' and e['id']=='ultra-research'): candidates.append((0 if overlap else 1,e['default_priority'],e,sorted(overlap)))
    candidates.sort(key=lambda x:(x[0],x[1],x[2]['id']))
    chosen=[]; seen=set()
    mandatory=set(route.get('required_reference_ids',[]))
    if profile.get('depth_class')=='ultra': mandatory.add('ultra-research')
    for ref in sorted(mandatory):
        item=next((x for x in candidates if x[2]['id']==ref),None)
        if item is None: raise ValueError('ULTRA_REFERENCE_MISSING: UNSUPPORTED_REQUIRED_REFERENCE: '+ref if ref=='ultra-research' else 'UNSUPPORTED_REQUIRED_REFERENCE: '+ref)
        chosen.append(item);seen.add(ref)
    # A typical reading budget may not erase a mandatory family/control.
    for fam in route.get('required_families',[]):
        item=next((x for x in candidates if x[2]['family']==fam),None)
        if item is None: raise ValueError('UNSUPPORTED_REQUIRED_FAMILY: '+fam)
        if item[2]['id'] not in seen: chosen.append(item);seen.add(item[2]['id'])
    for item in candidates:
        if len(chosen)>=max(limit,len(required)):break
        if item[2]['id'] not in seen:chosen.append(item);seen.add(item[2]['id'])
    out=[]
    for _,_,e,overlap in chosen:
        out.append({'reference_id':e['id'],'family':e['family'],'path':e['path'],'load_reason':'mandatory_method' if e['id'] in mandatory else ('gap_match' if overlap else 'family_entry'),'current_gap':','.join(overlap) if overlap else 'family_entry','profile_version':profile['profile_version'],'context_cost_class':e['context_cost_class']})

    return out

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('profile'); ap.add_argument('route'); ap.add_argument('--index',default=str(Path(__file__).resolve().parents[1]/'routing-index.json')); ap.add_argument('--gap-tag',action='append',default=[]); a=ap.parse_args()
    profile=json.loads(Path(a.profile).read_text()); route=json.loads(Path(a.route).read_text()); index=json.loads(Path(a.index).read_text())
    if route.get('profile_version')!=profile.get('profile_version'): print(json.dumps({'passed':False,'code':'STALE_ROUTE'},indent=2)); return 1
    try: selected=select(index,route,profile,a.gap_tag)
    except ValueError as e: print(json.dumps({'passed':False,'code':str(e)},indent=2)); return 1
    print(json.dumps({'passed':True,'selected_references':selected},indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
