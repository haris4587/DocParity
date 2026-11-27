# DocParity

DocParity helps maintainers check whether software documentation represents the implementation at a particular Git revision. A misleading CLI flag, stale setup command or unsupported security guarantee can lead users to take the wrong action. DocParity locks explicit claims, checks exact repository evidence, and records independently validated decisions on GenLayer.

**Outcomes:** ACCURATE, OUTDATED, MISLEADING, INCONCLUSIVE.

The dashboard reads finalized contract state and provides evidence quotations, deterministic checks, downloadable receipts, revision links and challenges. It submits real GenLayer writes with an EIP-1193 wallet, or prepares exact call inputs for GenLayer Studio's built-in wallet. It never requests a private key.

## Run locally

Website: https://docparity.mohamedansaf222.chatgpt.site

Contract: https://explorer-studio.genlayer.com/address/0x058F4Fb06c954085B7e2f41A2614A81d00D82a16

Requires Node.js 22+ and Python 3.11+.

```sh
npm ci
npm test
npm run build
npm run dev
```

`npm test` runs Python contract logic tests using an explicit GenLayer test double and JavaScript wallet/lifecycle tests. These are local tests, not network consensus proof. `npm run schema` uses the live Studionet GenVM schema endpoint. `genvm-lint check contracts/doc_parity.py` runs the GenVM linter and semantic validator when installed.

## Review a repository

1. Create a scope JSON using `public/example-scope.json`. Pin the documentation, implementation and test report with full 40-character Git commits. Provide up to six explicit claims with exact commands, parameter tokens, expected exit codes and output fragments.
2. Select **New assessment**, load or paste the scope, then **Lock assessment**. Scope and owner are immutable. The ID is SHA-256 of `lowercase(owner) + ':' + canonical(scope)`.
3. Open the assessment. Paste its manifest (see `public/example-manifest.json`) and **Lock evidence**. Each raw GitHub file has a role, byte length and SHA-256. Evidence is immutable; corrections require a new assessment.
4. **Run consensus review**. Every validator retrieves the pinned files, verifies their bytes, independently evaluates semantic support and agrees on stable per-claim decisions. The contract aggregates the result conservatively.
5. Inspect evidence quotations and checks. Download a receipt or challenge a specific concern. Challenges immediately make the effective verdict INCONCLUSIVE. A new review may resolve it; prior receipts remain accessible.

Use a browser wallet on Studionet (61999), or select **Studio built-in wallet**. In Studio mode the dashboard downloads a JSON call packet. Open the deployed contract in Studio, choose the named method, paste the named inputs, keep **Normal (Full Consensus)**, and send. Paste that transaction hash into the dashboard monitor. Studio's wallet is origin-isolated; the external dashboard cannot silently sign on its behalf.

## Evidence and verdict rules

Only public `raw.githubusercontent.com/<same-repository>/<full-commit>/<safe-path>` URLs are accepted. Required roles: docs, source, tests. Up to six files, 16,000 bytes per file, 40,000 total. The report uses `{"code_commit":"...","runs":[{"claim_id":"...","command":"...","exit_code":0,"output":"..."}]}`. Report revision and implementation revision are separate because committing a report changes the repository commit.

Deterministic checks verify the statement and command appear in docs, source contains declared parameter tokens, each claim has exactly one matching test run, and observed exit/output match expectations. Token presence alone cannot establish meaning. AI validators examine conditions, defaults, side effects and unsupported guarantees, with exact quotations grounded in all three roles for a non-INCONCLUSIVE result.

- **ACCURATE:** complete coverage, matching deterministic checks and semantic support for all scoped claims.
- **OUTDATED:** an obsolete command, parameter or expected result contradicts the implementation.
- **MISLEADING:** a materially unsupported capability or guarantee; this is not a finding about intent.
- **INCONCLUSIVE:** missing coverage/context, unavailable or incorrect bytes, semantic uncertainty, mismatched checks without a supported adverse finding, or a pending challenge.

Missing claim coverage or any INCONCLUSIVE claim takes precedence. Otherwise MISLEADING precedes OUTDATED; ACCURATE requires every check to pass. Rejected consensus or model failures do not create a successful receipt.

## Contract methods

| Method | Access | Purpose |
|---|---|---|
| `open_assessment(scope_json)` | Anyone | Lock scope; return content-derived assessment ID |
| `submit_evidence(case_id, manifest_json)` | Owner | Lock manifest once |
| `assess(case_id)` | Anyone | Review first round or an open challenge; maximum three rounds |
| `challenge(case_id, reason)` | Anyone | Flag an existing decision for bounded reassessment |
| `get_assessment(case_id)` | View | Scope, manifest, round count and effective verdict |
| `get_receipt(case_id, round_number)` | View | Immutable per-round evidence-linked receipt |
| `get_event(sequence)` | View | Append-only global event |
| `get_index(offset)` | View | Page of up to 20 IDs, global event count and chain head |

Receipts bind scope hash, manifest hash, previous receipt hash, challenge and decision. Events bind actor, payload, previous event hash and sequence. JSON hashing uses sorted keys, compact separators and ASCII escaping. This proves stored integrity, not truth of submitted evidence.

## Reproduce fixtures

The fixture repository contains a working `--name` argument, an obsolete `--uppercase` instruction and an unsupported encryption guarantee. `scripts/run-fixtures.py` executes only the fixed local fixture commands. Do not execute downloaded or untrusted source.

```sh
python scripts/run-fixtures.py
```

This writes a report for the current checked-out Git commit. Commit it afterward; use that later commit as `tests_commit` and the original source commit as `code_commit`. `scripts/prepare-examples.py` records the existing published fixture revisions; update those constants when intentionally publishing new examples.

## Trust boundaries and continued use

DocParity verifies selected documentation claims against supplied repository evidence; it does not audit the whole application, execute arbitrary code, prove test-log authenticity, or guarantee software security. A source commit is authoritative for repository contents, not for author identity or actual production behavior. Reproduce test outputs independently. Small excerpts can omit relevant behavior and should receive INCONCLUSIVE when insufficient.

Permissionless challenges are bounded to two reassessments after the first round. They can temporarily suppress an effective verdict and consume rounds. This is an explicit anti-overclaim tradeoff, not an abuse-proof dispute market. Create a new immutable review when evidence or scope changes. A practical continued use is comparing scoped release claims at each release commit and attaching receipt links to release notes.

See [SECURITY.md](SECURITY.md), [DEPLOYMENT.md](DEPLOYMENT.md), [EVIDENCE.md](EVIDENCE.md), and [SUBMISSION.md](SUBMISSION.md) for operating limits and the current verification status. Studionet is a development network and may reset.
