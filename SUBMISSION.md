# Project submission draft

**Project name:** DocParity

**Short description:** Evidence-linked verification of software documentation against commit-pinned implementation and reproducible test reports.

**Primary area:** Developer tooling / verification.

## Notes

DocParity addresses a release trust problem: users rely on documented commands, parameters and capability claims that may contradict the implementation. Maintainers lock explicit documentation claims and immutable Git revisions, then submit SHA-256/byte-bound documentation, source and test-report evidence. A GenLayer Intelligent Contract verifies command coverage, parameters, exit codes and expected outputs deterministically. Independent AI validators retrieve the same pinned evidence, reason about semantic support, verify exact quotations and agree on per-claim decisions. Results are ACCURATE, OUTDATED, MISLEADING or INCONCLUSIVE.

The dashboard reads finalized contract state, supports real provider-backed contract writes, tracks submission/consensus/finalization/execution separately, and supports Studio built-in wallet signing through exact call packets. Users inspect evidence quotations, challenge a decision, and retrieve append-only hash-linked receipts. Corrections require a new immutable assessment.

To use: open the dashboard, load a scope, lock it, submit its evidence manifest and run review; inspect or challenge the receipt. In Studio mode, download call inputs, sign with Normal (Full Consensus), then paste the transaction hash into the dashboard monitor.

This is scoped repository evidence verification, not arbitrary code execution, software certification or proof that committed test logs were honestly generated. Local tests, GenVM validation and actual Studionet transactions are documented in EVIDENCE.md, including rejected transactions and verification limits. Actual reviews include an ACCURATE claim, a challenged/reassessed receipt, and an adverse review with OUTDATED and MISLEADING claims.

## Supporting links

- Source: https://github.com/haris4587/DocParity
- Contract: https://explorer-studio.genlayer.com/address/0x058F4Fb06c954085B7e2f41A2614A81d00D82a16
- Deployment transaction: https://explorer-studio.genlayer.com/transactions/0xdfae0c0443b9c966bf60f3ed17507a0cbcb75cc47869a9bc7206955fc5400d4c
- First assessment: https://explorer-studio.genlayer.com/transactions/0xe9adab3c8a9e9e879873e31352ea9465c374fa0f95ec72387d9854faf6418553
- Final verification: https://github.com/haris4587/DocParity/blob/main/evidence/verified-live.json

**Website:** https://docparity.mohamedansaf222.chatgpt.site — verify the publication record in EVIDENCE.md and ensure reviewer access is public before submission.
