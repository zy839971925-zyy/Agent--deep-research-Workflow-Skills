#!/usr/bin/env python3
"""Pure live-context checks. The caller must supply authenticated observations.
Does not commit state, authenticate a principal, or verify external authorization.
"""
from datetime import datetime,timezone
from runtime_core import validate_worker_proposal

def verify_submission_context(plan,proposal,ledger,authenticated_executor,now,authorize):
    """Return (allowed, reasons). authorize is a trusted host function, not worker JSON.
    Atomic compare-and-swap and a cancellation fence remain mandatory at commit.
    """
    reasons=[]
    if validate_worker_proposal(plan,proposal,current_state_version=ledger.get('state_version')): reasons.append('proposal_invalid')
    if ledger.get('plan_id')!=plan.get('plan_id') or ledger.get('plan_version')!=plan.get('plan_version'): reasons.append('ledger_plan_mismatch')
    entry=next((n for n in ledger.get('nodes',[]) if n.get('node_id')==proposal.get('node_id')),None)
    if not entry: reasons.append('node_missing'); return False,reasons
    if entry.get('effective_status') not in ('running',): reasons.append('lifecycle_not_admissible')
    if not authenticated_executor or authenticated_executor!=proposal.get('executor_id') or entry.get('executor_id')!=authenticated_executor: reasons.append('executor_mismatch')
    if not entry.get('active_attempt_id') or entry['active_attempt_id']!=proposal.get('attempt_id'): reasons.append('attempt_mismatch')
    if entry.get('node_contract_hash')!=proposal.get('node_contract_hash'): reasons.append('contract_mismatch')
    if not entry.get('lease_id'): reasons.append('lease_missing')
    if entry.get('lease_id'):
        try:
            expiry=datetime.fromisoformat(entry['lease_expires_at'].replace('Z','+00:00'))
            if expiry.tzinfo is None or now.tzinfo is None or expiry<=now: reasons.append('lease_expired_or_ambiguous')
        except (KeyError,ValueError,TypeError): reasons.append('lease_unverified')
    try: approved=callable(authorize) and authorize(proposal,entry,plan) is True
    except Exception: approved=False
    if not approved: reasons.append('host_authorization_unverified')
    return not reasons,reasons
