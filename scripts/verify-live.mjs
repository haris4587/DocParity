// Public read-only verification. No secret material or transaction submissions.
import fs from 'node:fs';import crypto from 'node:crypto';
import {createClient} from 'genlayer-js';import {studionet} from 'genlayer-js/chains';import {TransactionHashVariant} from 'genlayer-js/types';
import {transactionState} from '../src/wallet.mjs';
const c=createClient({chain:studionet}),d=JSON.parse(fs.readFileSync('evidence/deployment.json'));
const json=x=>JSON.stringify(x,(_,v)=>typeof v==='bigint'?String(v):v,2)+'\n';
let last=0;
async function paced(fn){const delay=last+4000-Date.now();if(delay>0)await new Promise(r=>setTimeout(r,delay));last=Date.now();return fn();}
const read=async(fn,args=[])=>JSON.parse(await paced(()=>c.readContract({address:d.address,functionName:fn,args,transactionHashVariant:TransactionHashVariant.LATEST_FINAL})));
const remote=await paced(()=>c.getContractCode(d.address));
const bytes=remote.startsWith('0x')?Buffer.from(remote.slice(2),'hex'):Buffer.from(remote);
if(!bytes.equals(fs.readFileSync('contracts/doc_parity.py')))throw Error('Deployed source does not match repository source.');
const transactions=[];
for(const t of d.transactions){
 const r=await paced(()=>c.getTransaction({hash:t.hash}));
 const node=n=>({mode:n.mode,vote:n.vote,execution_result:n.execution_result,nondet_disagree:n.nondet_disagree,model:n.node_config?.primary_model?.model,eq_outputs:n.eq_outputs});
 const p={hash:r.hash,from_address:r.from_address,to_address:r.to_address,statusName:r.statusName,result_name:r.result_name,leader_only:r.leader_only,txExecutionResultName:r.txExecutionResultName,consensus_data:{votes:r.consensus_data?.votes,leader_receipt:r.consensus_data?.leader_receipt?.map(node),validators:r.consensus_data?.validators?.map(node)}};
 fs.writeFileSync('evidence/tx-'+t.action+'.json',json(p));
 if(!transactionState(r).success||r.leader_only!==false)throw Error('Not finalized with successful full-consensus execution: '+t.action);
 transactions.push({action:t.action,hash:t.hash,status:r.statusName,result:r.result_name,leader_only:r.leader_only});
}
const index=await read('get_index',[0]),events=[];
let head='0'.repeat(64);
for(let i=1;i<=index.events;i++){
 const e=await read('get_event',[i]);const {hash,...body}=e;
 const canon=x=>JSON.stringify(Object.fromEntries(Object.entries(x).sort(([a],[b])=>a.localeCompare(b))));
 // Python canonical JSON sorts recursively; export verifier below uses a recursive serializer.
 function canonical(x){if(x===null||typeof x!=='object')return JSON.stringify(x).replace(/[\u007f-\uffff]/g,c=>'\\u'+c.charCodeAt(0).toString(16).padStart(4,'0'));if(Array.isArray(x))return '['+x.map(canonical).join(',')+']';return '{'+Object.keys(x).sort().map(k=>canonical(k)+':'+canonical(x[k])).join(',')+'}';}
 const expected=crypto.createHash('sha256').update(canonical(body)).digest('hex');
 if(e.previous!==head||hash!==expected)throw Error('Broken event chain at '+i);head=hash;events.push(e);
}
if(head!==index.head)throw Error('Event chain head mismatch');
const cases={};
for(const id of d.cases||[]){const state=await read('get_assessment',[id]);const receipts=[];for(let n=1;n<=state.rounds;n++)receipts.push(await read('get_receipt',[id,n]));cases[id]={...state,receipts};}
fs.writeFileSync('evidence/events-live.json',json(events));fs.writeFileSync('evidence/cases-live.json',json(cases));
const summary={verified_at:new Date().toISOString(),address:d.address,source_matches:true,source_sha256:crypto.createHash('sha256').update(bytes).digest('hex'),event_chain_valid:true,index,transactions,outcomes:Object.fromEntries(Object.entries(cases).map(([id,c])=>[id,c.effective_verdict]))};
fs.writeFileSync('evidence/verified-live.json',json(summary));console.log(json(summary));
