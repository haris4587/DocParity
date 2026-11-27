"""Bind locally reproduced fixtures to their immutable public Git revisions."""
import pathlib,json,hashlib
root=pathlib.Path(__file__).resolve().parents[1]
source='c268f535f168db8712b1cb5825bb611c6bed0a44'
reports='afc01cc71c697e6bbfd2b1739dba56e69a72ba54'
base={'repository':'haris4587/DocParity','docs_commit':source,'code_commit':source,'tests_commit':reports}
claims=[{'id':'greeting','statement':'The --name parameter selects the person to greet.','command':'python fixtures/cli.py --name Ada','parameters':['--name'],'expected_exit':0,'expected_output':'Hello, Ada!'}, {'id':'uppercase','statement':'The --uppercase parameter prints the greeting in uppercase.','command':'python fixtures/cli.py --uppercase','parameters':['--uppercase'],'expected_exit':0,'expected_output':'HELLO, DEVELOPER!'}, {'id':'encryption','statement':'The greeting command encrypts the output before printing it.','command':'python fixtures/cli.py --name Ada','parameters':['--name'],'expected_exit':0,'expected_output':'Hello, Ada!'}]
files=[]
for role,path in [('docs','fixtures/usage.md'),('source','fixtures/cli.py'),('tests','fixtures/test-output.json')]:
    body=(root/path).read_bytes();revision=reports if role=='tests' else source
    files.append({'role':role,'url':f'https://raw.githubusercontent.com/haris4587/DocParity/{revision}/{path}','sha256':hashlib.sha256(body).hexdigest(),'bytes':len(body)})
manifest={'files':files}
for n,c in enumerate(claims):
    scope=dict(base,title=['Greeting parameter behavior','Obsolete uppercase flag','Unsupported encryption guarantee'][n],claims=[c])
    (root/f'fixtures/scope-{c["id"]}.json').write_text(json.dumps(scope,indent=2)+'\n')
    if n==0:(root/'public/example-scope.json').write_text(json.dumps(scope,indent=2)+'\n')
(root/'public/example-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(root/'fixtures/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Prepared three independent scoped reviews and a pinned manifest.')
