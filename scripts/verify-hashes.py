"""Verify exported on-chain receipt, scope, manifest and event commitments offline."""
import json,hashlib,pathlib
root=pathlib.Path(__file__).resolve().parents[1]
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()
cases=json.loads((root/'evidence/cases-live.json').read_text());count=0
for key,c in cases.items():
    assert digest(c['scope'])==c['scope_hash']
    assert hashlib.sha256((c['owner'].lower()+':'+json.dumps(c['scope'],sort_keys=True,separators=(',',':'),ensure_ascii=True)).encode()).hexdigest()==key
    previous='0'*64
    for n,r in enumerate(c['receipts'],1):
        body={k:v for k,v in r.items() if k!='hash'}
        assert digest(body)==r['hash'] and r['previous_receipt']==previous
        assert r['case_id']==key and r['round']==n and r['scope_hash']==digest(c['scope']) and r['manifest_hash']==digest(c['manifest'])
        previous=r['hash'];count+=1
    assert previous==c['receipt_hash']
head='0'*64
events=json.loads((root/'evidence/events-live.json').read_text())
for n,e in enumerate(events,1):
    assert e['sequence']==n and e['previous']==head and digest({k:v for k,v in e.items() if k!='hash'})==e['hash']
    head=e['hash']
print(f'Verified {len(cases)} locked scopes/manifests, {count} receipt hashes and {len(events)} chained events.')
