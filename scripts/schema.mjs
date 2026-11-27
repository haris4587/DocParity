import fs from 'node:fs';
import {createClient} from 'genlayer-js';
import {studionet} from 'genlayer-js/chains';
const c=createClient({chain:studionet});
console.log('Studionet RPC:',studionet.rpcUrls.default.http[0]);
const schema=await c.getContractSchemaForCode(fs.readFileSync('contracts/doc_parity.py','utf8'));
fs.writeFileSync('evidence/schema.json',JSON.stringify(schema,null,2)+'\n');
console.log(JSON.stringify(schema,null,2));
