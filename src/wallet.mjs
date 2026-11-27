export const CHAIN_ID='0xf22f';
export async function connectWallet(provider){
 if(!provider?.request)throw Error('No browser wallet found. Use GenLayer Studio, or open this page with MetaMask installed.');
 const accounts=await provider.request({method:'eth_requestAccounts'});
 if(!Array.isArray(accounts)||!/^0x[0-9a-fA-F]{40}$/.test(accounts[0]||''))throw Error('Wallet returned no valid account.');
 if(String(await provider.request({method:'eth_chainId'})).toLowerCase()!==CHAIN_ID){
  try{await provider.request({method:'wallet_switchEthereumChain',params:[{chainId:CHAIN_ID}]});}
  catch(e){if(e.code!==4902)throw e;await provider.request({method:'wallet_addEthereumChain',params:[{chainId:CHAIN_ID,chainName:'GenLayer Studionet',nativeCurrency:{name:'GEN',symbol:'GEN',decimals:18},rpcUrls:['https://studio.genlayer.com/api'],blockExplorerUrls:['https://explorer-studio.genlayer.com']}]});await provider.request({method:'wallet_switchEthereumChain',params:[{chainId:CHAIN_ID}]});}
 }
 if(String(await provider.request({method:'eth_chainId'})).toLowerCase()!==CHAIN_ID)throw Error('Switch to GenLayer Studionet before signing.');
 return accounts[0];
}
export function transactionState(tx){
 const status=String(tx.statusName||tx.status_name||tx.status||'PENDING').toUpperCase();
 const list=tx.consensus_data?.leader_receipt;
 const leader=Array.isArray(list)?list.filter(r=>r.mode==='leader'||r.vote!=='idle').at(-1):list;
 const success=status==='FINALIZED'&&(tx.txExecutionResultName==='FINISHED_WITH_RETURN'||(tx.result_name==='MAJORITY_AGREE'&&leader?.execution_result==='SUCCESS')||tx.result_name==='SUCCESS')&&!['ERROR','CONTRACT_ERROR'].includes(leader?.execution_result);
 return {status,success,terminal:['FINALIZED','UNDETERMINED','CANCELED','CANCELLED','REJECTED','FAILED'].includes(status)};
}
export async function submitOnce({client,address,functionName,args,onHash}){
 const hash=await client.writeContract({address,functionName,args,leaderOnly:false,value:0n});
 onHash(hash);return hash;
}
