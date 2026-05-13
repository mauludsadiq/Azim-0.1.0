# Azim

Deterministic distributed AI training on FARD.

Azim is a training system built on deterministic execution, cryptographic receipts, replay-verifiable distributed computation, validator-supervised optimization, and lawful output constraints. Pure FARD — no Python, no external ML libraries, 14,683 lines of code.

-----

## Training Results

Full OpenWebText classifier run. All 80 shards. 15 hours. MacBook Pro. Pure FARD.

```
Shard  0:  0.7605
Shard 20:  0.0981
Shard 40:  0.0491
Shard 60:  0.0327
Shard 79:  0.0244
```

96.8% loss reduction. Every step cryptographically receipted.

LM objective run (next-token prediction). All 80 shards complete.

```
Mean loss:    4.7927  (below random baseline 4.8598)
Final loss:   4.1237  (-0.74 vs random)
Below random: 47/80 shards
```

GitHub corpus: 44 verified executable files, 14,571 tokens, trained 132 steps.

-----

## Status

|Milestone                                   |Status|
|--------------------------------------------|------|
|Deterministic runtime (FARD)                |done  |
|Cryptographic receipt chain                 |done  |
|Full OWT training runs                      |done  |
|linalg native ops (28x speedup)             |done  |
|Multi-language tokenizer (159 tokens)       |done  |
|BPE tokenizer (500 merges, vocab 600)       |done  |
|Verifier-gated self-training loop           |done  |
|Scale gate with language diversity          |done  |
|Architecture (d_model=32, n_layers=2)       |done  |
|Blockwise multi-direction SPSA all weights  |done  |
|Deterministic samplers                      |done  |
|CLI + benchmark suite (4/4)                 |done  |
|Language control tokens                     |done  |
|Hybrid orchestration                        |done  |
|Execution verifiers (Python, JS, Rust, FARD)|done  |
|Unit-test harness                           |done  |
|HumanEval runner                            |done  |
|GitHub corpus acquisition                   |done  |
|Scale to d_model=128 (cloud GPU)            |next  |
|HumanEval benchmark scores                  |next  |

-----

## Phase C — Code as the Primary Signal

The acceptance manifold: generate → execute → test → accept. Only runnable code enters training.

### Execution Verifiers

```
Python:     python3 candidate.py       — stdout/stderr receipted
JavaScript: node candidate.js          — stdout/stderr receipted
Rust:       rustc + run binary         — stdout/stderr receipted
FARD:       fardrun run + receipt chain — full receipt verification
```

### Unit-Test Harness

```
run_python_with_tests(source, tests)   — correct code passes, wrong code fails
run_js_with_tests(source, tests)       — same pattern
run_rust_with_tests(source, tests)     — #[cfg(test)] integration
```

### HumanEval Runner

```
run_problem(problem, candidate)        — pass/fail + receipt
run_suite(problems, candidate_fn)      — pass_rate across 164 problems
```

### GitHub Corpus Acquisition

```
github_search(lang, min_stars)         — find repos via API
github_tree(owner, repo)               — list files
fetch_raw(owner, repo, path)           — fetch content
acquire_and_pack(owner, repo, ...)     — fetch → execute → accept → JSONL
```

Acquired from algorithm repos (self-contained, no external deps):

```
TheAlgorithms/Python:          13 accepted, 5,168 tokens
keon/algorithms:               13 accepted, 4,757 tokens
TheAlgorithms/JavaScript:       9 accepted, 4,300 tokens
interactive-coding-challenges:  9 accepted,   346 tokens
Total: 44 files, 14,571 tokens, receipted shard
```

-----

## Roadmap to GPT-2 Scale

|Phase|Params|GPU hours|Target                               |
|-----|------|---------|-------------------------------------|
|A1   |6M    |~50      |Real language patterns, code training|
|A2   |30M   |~200     |HumanEval meaningful scores          |
|A3   |85M   |~500     |GPT-2 small equivalent               |

Total compute: ~1,050 A100-hours, ~$1,575.

-----

## CLI

```
fardrun run --program azim.fard --out <out> -- generate --prompt "..." --mode topk
fardrun run --program run_benchmark.fard --out out/benchmark
```

-----

## Architecture

```
d_model: 32, n_layers: 2, vocab: 600 (BPE), params: ~50,000
Blockwise multi-direction SPSA — all weights — deterministic — receipted
```

-----

## Test Coverage

191 test files. 0 failures.

-----

## Repository Structure

```
packages/azim_trial/         — core LM training system
packages/azim_code/
  verifier.fard              — execution verifiers (Python, JS, Rust, FARD)
  test_harness.fard          — unit-test runner
  humaneval_runner.fard      — HumanEval pass/fail with receipts
  corpus_acquire.fard        — GitHub corpus acquisition
  tokenizer.fard             — 159-token multi-language tokenizer
  lang_detect.fard           — language detection
  corpus_packer.fard         — corpus with language control tokens
  multilang_generation_wrapper.fard
  hybrid_proposer.fard
  hybrid_loop.fard
  scale_gate.fard
  loop_run.fard

azim.fard                    — CLI
run_benchmark.fard           — benchmark suite
main_lm.fard                 — OWT training
build_corpus_v2.fard         — GitHub corpus acquisition
pack_full_corpus.fard        — merge shards

tests/
  test_*.fard  (191 files)
```

-----

## License

MUI