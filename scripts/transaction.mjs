import fs from 'node:fs';import {createClient} from 'genlayer-js';import {studionet} from 'genlayer-js/chains';
const c=createClient({chain:studionet});const r=await c.getTransaction({hash:process.argv[2]});
const node=n=>({mode:n.mode,vote:n.vote,execution_result:n.execution_result,nondet_disagree:n.nondet_disagree,model:n.node_config?.primary_model?.model,eq_outputs:n.eq_outputs,result:n.result?.payload?.readable||n.result,genvm_result:n.genvm_result,stderr:n.stderr});
const out={hash:r.hash,statusName:r.statusName,result_name:r.result_name,leader_only:r.leader_only,consensus_data:{votes:r.consensus_data?.votes,leader_receipt:r.consensus_data?.leader_receipt?.map(node),validators:r.consensus_data?.validators?.map(node)}};
fs.writeFileSync('evidence/'+(process.argv[3]||'transaction')+'.json',JSON.stringify(out,(_,v)=>typeof v==='bigint'?String(v):v,2)+'\n');console.log(JSON.stringify(out,(_,v)=>typeof v==='bigint'?String(v):v,2));
