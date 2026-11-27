# Deployment and operation

- Network: GenLayer Studionet, chain ID **61999**.
- RPC: https://studio.genlayer.com/api
- Contract: **0x058F4Fb06c954085B7e2f41A2614A81d00D82a16**.
- Explorer: https://explorer-studio.genlayer.com/address/0x058F4Fb06c954085B7e2f41A2614A81d00D82a16
- Deployer: Studio built-in account `0xcD72fA5B6A496d84B4A10bCFF31D3B7c12346a9e`.
- Constructor takes no arguments. Deployment used **Normal (Full Consensus)**.
- The public metadata lives in `src/deployment.json` and `evidence/deployment.json`; no secret environment variables are needed.

## Deploy the contract again

1. Import the exact `contracts/doc_parity.py` file into https://studio.genlayer.com/contracts.
2. Select the source, open Run and Debug using the Studio sidebar, and retain Normal (Full Consensus).
3. Deploy with the built-in account. Wait for finalization and verify successful execution, not status alone.
4. Update both public metadata files with the new address and deployment transaction. Do not silently upgrade a contract that reviewers are already using.
5. Run the fixtures through the locked scope/evidence/review flow and export public receipts.

## Publish the dashboard as a ChatGPT Site

The dashboard is published at https://docparity.mohamedansaf222.chatgpt.site. Publication status is recorded in EVIDENCE.md. `.openai/hosting.json` identifies this exact Site and its static `dist` output. Sites publication saves the pushed source commit and its matching deployment archive.

```sh
npm ci
npm test
npm run build
```

No server signer or secret environment variables are used. The website calls Studionet directly; MetaMask handles signatures, or users sign the prepared calls inside Studio. Do not publish private keys. An optional Netlify configuration remains available in the repository for portability; Netlify publication was not performed.

## Verify an existing deployment

```sh
node scripts/verify-live.mjs
```

This read-only exporter compares deployed source bytes with the local contract, verifies full-consensus transaction success and finality, and checks the global event hash chain. It exports finalized case state and receipts. It does not submit transactions. Network errors or pending/rejected writes fail verification; do not claim those are successful tests.

Public reads are paced to respect Studio's shared rate limits. Avoid running multiple exporter instances or repeatedly refreshing several Studio tabs. A timeout after a submitted hash is not a failed submission: resume tracking the existing hash.

`npm run dev` serves the dashboard locally. `src/deployment.json` selects the deployed contract. A browser wallet must be on Studionet; the Studio workflow signs in Studio and tracks the resulting hash from the dashboard. A MetaMask extension is not required for Studio use.
