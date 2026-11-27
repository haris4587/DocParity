import unittest, types, sys, json, pathlib, hashlib
from copy import deepcopy
ROOT=pathlib.Path(__file__).resolve().parents[1]
class UserError(Exception): pass
class Return:
    def __init__(self, calldata): self.calldata=calldata
identity=lambda fn: fn
fake=types.ModuleType('genlayer')
fake.gl=types.SimpleNamespace(Contract=object,public=types.SimpleNamespace(write=identity,view=identity),vm=types.SimpleNamespace(UserError=UserError,Return=Return),message=types.SimpleNamespace(sender_address='0x'+'a'*40))
fake.TreeMap=dict; fake.DynArray=list; fake.u256=int
sys.modules['genlayer']=fake
ns={};exec((ROOT/'contracts/doc_parity.py').read_text(),ns)
class ContractTests(unittest.TestCase):
    def setUp(self):
        fake.gl.message.sender_address='0x'+'a'*40
        self.s={'title':'Greeting','repository':'haris4587/DocParity','docs_commit':'a'*40,'code_commit':'b'*40,'tests_commit':'c'*40,'claims':[{'id':'greeting','statement':'Name selects recipient.','command':'python cli.py --name Ada','parameters':['--name'],'expected_exit':0,'expected_output':'Hello, Ada!'}]}
        self.files=[{'role':'docs','content':'Name selects recipient. python cli.py --name Ada'},{'role':'source','content':"add_argument('--name'); print('Hello, Ada!')"},{'role':'tests','content':json.dumps({'code_commit':'b'*40,'runs':[{'claim_id':'greeting','command':'python cli.py --name Ada','exit_code':0,'output':'Hello, Ada!'}]})}]
        self.m={'files':[{'role':f['role'],'url':'https://raw.githubusercontent.com/haris4587/DocParity/'+self.s[{'docs':'docs_commit','source':'code_commit','tests':'tests_commit'}[f['role']]]+'/'+f['role']+'.txt','bytes':len(f['content'].encode()),'sha256':hashlib.sha256(f['content'].encode()).hexdigest()} for f in self.files]}
        self.r={'claims':[{'id':'greeting','verdict':'ACCURATE','doc_quote':'Name selects recipient.','source_quote':"add_argument('--name')",'test_quote':'Hello, Ada!','reason':'Implementation and test support the scoped statement.'}]}
        self.c=ns['DocParity']();self.c.cases={};self.c.receipts={};self.c.events={};self.c.case_ids=[]
        def get(url):
            i=[x['url'] for x in self.m['files']].index(url)
            return types.SimpleNamespace(status=200,body=self.files[i]['content'].encode())
        fake.gl.nondet=types.SimpleNamespace(web=types.SimpleNamespace(get=get),exec_prompt=lambda *a,**k:deepcopy(self.r))
        def consensus(leader,validator):
            result=leader();self.assertTrue(validator(Return(result)));return result
        fake.gl.vm.run_nondet_unsafe=consensus
    def open(self): return self.c.open_assessment(json.dumps(self.s))
    def submit(self):
        i=self.open();self.c.submit_evidence(i,json.dumps(self.m));return i
    def test_valid_scope(self): ns['validate_scope'](self.s)
    def test_full_sha_required(self):
        self.s['code_commit']='main'
        with self.assertRaises(UserError): ns['validate_scope'](self.s)
    def test_boolean_exit_rejected(self):
        self.s['claims'][0]['expected_exit']=True
        with self.assertRaises(UserError): ns['validate_scope'](self.s)
    def test_duplicate_claims_rejected(self):
        self.s['claims']*=2
        with self.assertRaises(UserError): ns['validate_scope'](self.s)
    def test_duplicate_json_keys_rejected(self):
        with self.assertRaises(UserError): ns['parse']('{"a":1,"a":2}',100)
    def test_branch_evidence_rejected(self):
        self.m['files'][0]['url']=self.m['files'][0]['url'].replace('a'*40,'main')
        with self.assertRaises(UserError): ns['validate_manifest'](self.m,self.s)
    def test_path_traversal_rejected(self):
        self.m['files'][0]['url']+='/../secret'
        with self.assertRaises(UserError): ns['validate_manifest'](self.m,self.s)
    def test_foreign_repository_rejected(self):
        self.m['files'][0]['url']=self.m['files'][0]['url'].replace('haris4587','evil')
        with self.assertRaises(UserError): ns['validate_manifest'](self.m,self.s)
    def test_body_size_cap(self):
        self.m['files'][0]['bytes']=16001
        with self.assertRaises(UserError): ns['validate_manifest'](self.m,self.s)
    def test_missing_role(self):
        self.m['files'][0]['role']='source'
        with self.assertRaises(UserError): ns['validate_manifest'](self.m,self.s)
    def test_deterministic_checks(self): self.assertTrue(all(v for k,v in ns['deterministic'](self.s,self.files)[0].items()))
    def test_wrong_report_revision(self):
        self.files[2]['content']=self.files[2]['content'].replace('b'*40,'d'*40)
        with self.assertRaises(UserError): ns['deterministic'](self.s,self.files)
    def test_duplicate_run_inconclusive(self):
        d=json.loads(self.files[2]['content']);d['runs']*=2;self.files[2]['content']=json.dumps(d)
        checks=ns['deterministic'](self.s,self.files)
        self.assertEqual(ns['aggregate'](self.r['claims'],checks),'INCONCLUSIVE')
    def test_false_quote_rejected(self):
        self.r['claims'][0]['source_quote']='made up encryption'
        with self.assertRaises(UserError): ns['check_result'](self.r,self.s,self.files)
    def test_missing_claim_rejected(self):
        self.r['claims']=[]
        with self.assertRaises(UserError): ns['check_result'](self.r,self.s,self.files)
    def test_outcome_precedence(self):
        checks=ns['deterministic'](self.s,self.files)
        for label in ['ACCURATE','OUTDATED','MISLEADING','INCONCLUSIVE']:
            self.assertEqual(ns['aggregate']([{'verdict':label}],checks),label)
    def test_owner_only_submission(self):
        i=self.open();fake.gl.message.sender_address='0x'+'f'*40
        with self.assertRaises(UserError): self.c.submit_evidence(i,json.dumps(self.m))
    def test_scope_immutable(self):
        self.open()
        with self.assertRaises(UserError): self.open()
    def test_evidence_immutable(self):
        i=self.submit()
        with self.assertRaises(UserError): self.c.submit_evidence(i,json.dumps(self.m))
    def test_lifecycle_and_hash_chain(self):
        i=self.submit();self.c.assess(i)
        self.assertEqual(json.loads(self.c.get_assessment(i))['effective_verdict'],'ACCURATE')
        self.c.challenge(i,'Check whether the default is covered.')
        self.assertEqual(json.loads(self.c.get_assessment(i))['effective_verdict'],'INCONCLUSIVE')
        self.c.assess(i)
        one=json.loads(self.c.get_receipt(i,1));two=json.loads(self.c.get_receipt(i,2))
        self.assertEqual(two['previous_receipt'],one['hash'])
        for n in range(1,self.c.count+1):
            e=json.loads(self.c.get_event(n));h=e.pop('hash');self.assertEqual(h,ns['sha'](ns['canon'](e)))
    def test_no_unbounded_reassessment(self):
        i=self.submit();self.c.assess(i)
        with self.assertRaises(UserError): self.c.assess(i)
        for _ in range(2): self.c.challenge(i,'Recheck exact behavior.');self.c.assess(i)
        with self.assertRaises(UserError): self.c.challenge(i,'Fourth round')
    def test_hash_failure_inconclusive(self):
        i=self.submit();self.files[0]['content']+=' altered';self.c.assess(i)
        self.assertEqual(json.loads(self.c.get_assessment(i))['verdict'],'INCONCLUSIVE')
    def test_malicious_leader_cannot_forge_quotes(self):
        i=self.submit()
        def consensus(leader,validator):
            r=json.loads(leader());r['claims'][0]['source_quote']='FORGED'
            self.assertFalse(validator(Return(json.dumps(r))))
            return leader()
        fake.gl.vm.run_nondet_unsafe=consensus;self.c.assess(i)
    def test_validator_disagreement_rejected(self):
        i=self.submit()
        def consensus(leader,validator):
            r=leader();self.r['claims'][0]['verdict']='OUTDATED'
            self.assertFalse(validator(Return(r)));return r
        fake.gl.vm.run_nondet_unsafe=consensus;self.c.assess(i)
    def test_index_pagination(self):
        self.open();self.assertEqual(json.loads(self.c.get_index(0))['total'],1)
        with self.assertRaises(UserError): self.c.get_index(-1)
