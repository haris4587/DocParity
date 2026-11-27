# Verification evidence

Local tests and actual network execution are distinct. The fixture evidence is deliberately small and reproducible; its test logs are repository assertions, not authenticated CI attestations.

| Check | Evidence |
|---|---|
| Contract logic and adversarial tests | 25 passing Python unit tests, `evidence/tests.txt` |
| Wallet and transaction lifecycle tests | 11 passing JavaScript tests, `evidence/tests.txt` |
| Production build | `evidence/build.txt` |
| GenVM lint and semantic validation | `evidence/genvm-check.txt` |
| Live Studionet schema extraction | `evidence/schema.json` and `evidence/schema-check.txt` |
| Deployed source equality | `evidence/verified-live.json` |
| Full-consensus successful transactions | `evidence/tx-*.json` projections; original hashes in `evidence/deployment.json` |
| Finalized receipt and global hash chain | `evidence/cases-live.json`, `evidence/events-live.json` |
| Rejected reassessment | `evidence/reassess-rejected.json`; invalid evidence quotation was rejected, with no accepted receipt |

The first live assessment returned ACCURATE with exact documentation, source and report quotations. The browser dashboard independently tracked its transaction to FINALIZED, checked successful execution, loaded the finalized ledger and displayed the receipt. An evidence-specific challenge then made its effective verdict INCONCLUSIVE while preserving the old receipt. The challenged assessment was successfully reassessed as ACCURATE in round 2. A second review returned MISLEADING overall, with OUTDATED for the obsolete --uppercase flag and MISLEADING for the unsupported encryption guarantee. Eight successful full-consensus transactions finalized. The source bytes, two locked scopes/manifests, three receipt hashes and eight chained events were verified. One rejected reassessment is preserved separately; its ungrounded quotation produced no accepted receipt. The exact transaction outcomes are recorded in `evidence/verified-live.json`.

Browser QA verified Studio signing, the live ledger, review detail, expanded quotations/checks, successful transaction tracking, and safe handling of a rejected consensus transaction. MetaMask was not installed in the browser: its EIP-1193 account, network-switch/add, rejection and submission paths were tested with explicit provider doubles. No live MetaMask signature is claimed. Studio's built-in account was used for actual signatures.

ChatGPT Site publication was confirmed successful at https://docparity.mohamedansaf222.chatgpt.site. The current access policy is owner-only until the owner requests public reviewer access. Netlify publication was not performed. No mobile-device test, video or public social post is claimed.

The transaction exports retain the decision-relevant public RPC fields while omitting repeated binary/state/log payloads. Re-run `node scripts/verify-live.mjs` to fetch and verify the current finalized state. Studionet can reset; receipts and on-chain links are development evidence rather than production guarantees.
