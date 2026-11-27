"""Execute fixed local fixture commands; never executes downloaded evidence."""
import subprocess, json, pathlib
rev = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
runs=[]
for claim, args in [('greeting',['--name','Ada']),('uppercase',['--uppercase']),('encryption',['--name','Ada'])]:
    cmd=['python','fixtures/cli.py',*args]
    p=subprocess.run(cmd,capture_output=True,text=True,timeout=10)
    runs.append({'claim_id':claim,'command':' '.join(cmd),'exit_code':p.returncode,'output':p.stdout+p.stderr})
pathlib.Path('fixtures/test-output.json').write_text(json.dumps({'code_commit':rev,'runs':runs},indent=2)+'\n')
print('Captured',len(runs),'fixture runs at',rev)
