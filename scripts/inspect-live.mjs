import fs from 'node:fs';import crypto from 'node:crypto';
import {createClient} from 'genlayer-js';import {studionet} from 'genlayer-js/chains';import {TransactionHashVariant} from 'genlayer-js/types';
const c=createClient({chain:studionet}),d=JSON.parse(fs.readFileSync('evidence/deployment.json'));
const fn=process.argv[2]||'get_index',args=JSON.parse(process.argv[3]||'[0]');
const raw=await c.readContract({address:d.address,functionName:fn,args,transactionHashVariant:TransactionHashVariant.LATEST_FINAL});console.log(raw);
