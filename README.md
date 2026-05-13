# Azim

Deterministic distributed AI training on FARD.

Azim is a training system built on deterministic execution, cryptographic receipts, replay-verifiable distributed computation, validator-supervised optimization, and lawful output constraints. Pure FARD — no Python, no external ML libraries, 14,357 lines of code.

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

Benchmark suite: 4/4 passing. HumanEval runner: pass/fail receipted.

-----

## Status

|Milestone                                                |Status|
|---------------------------------------------------------|------|
|Deterministic runtime (FARD)                             |done  |
|Cryptographic receipt chain                              |done  |
|Full OWT training runs (classifier + LM)                 |done  |
|Neural path authoritative                                |done  |
|linalg native ops (28x speedup)                          |done  |
|Multi-language tokenizer (159 tokens)                    |done  |
|BPE tokenizer (500 merges, vocab 600)                    |done  |
|Verifier-gated self-training loop                        |done  |
|Scale gate with language diversity                       |done  |
|Architecture (d_model=32, n_layers=2)                    |done  |
|Blockwise multi-direction SPSA all weights               |done  |
|Deterministic samplers (greedy, top-k, top-p)            |done  |
|CLI + benchmark suite                                    |done  |
|Multi-language verifier (syntax)                         |done  |
|Language control tokens                                  |done  |
|Hybrid orchestration                                     |done  |
|**Phase C: Execution verifiers (Python, JS, Rust, FARD)**|done  |
|**Phase C: Unit-test harness**                           |done  |
|**Phase C: HumanEval runner**                            |done  |
|Corpus acquisition from verified repos                   |next  |
|Scale to d_model=128 (6M params, cloud GPU)              |next  |

-----

## Phase C — Code as the Primary Signal

The acceptance manifold has changed. A candidate must now actually execute and pass tests — not just parse.

### Execution Verifiers

```
Python:     python3 candidate.py       — runs, receipts stdout/stderr
JavaScript: node candidate.js          — runs, receipts stdout/stderr
Rust:       rustc compile + run binary — runs, receipts stdout/stderr
FARD:       fardrun run + receipt chain — executes, verifies receipts
```

All four confirmed: `stdout: "42\n"`, `exit_code: 0`, `accepted: true`.

### Unit-Test Harness

```
run_python_with_tests(source, tests, ...)   — appends tests, runs python3
run_js_with_tests(source, tests, ...)       — appends tests, runs node
run_rust_with_tests(source, tests, ...)     — wraps in #[cfg(test)], rustc --test
```

Correct code passes. Wrong code fails. Both outcomes receipted.

### HumanEval Runner

164 Python problems. Each with prompt, candidate solution, and unit tests.

```
run_problem(problem, candidate, out_dir)    — pass/fail + receipt
run_suite(problems, candidate_fn, out_dir)  — pass_rate across suite
```

Correct solution passes. Wrong solution (`return False`) fails. Pass rate computed and receipted.

-----

## Roadmap to GPT-2 Scale

|Phase|Params|GPU hours|Target                       |
|-----|------|---------|-----------------------------|
|A1   |6M    |~50      |Real language patterns emerge|
|A2   |30M   |~200     |HumanEval meaningful scores  |
|A3   |85M   |~500     |GPT-2 small equivalent       |

Total: ~1,050 A100-hours, ~$1,575. Compute budget within grant ask.

HumanEval is the benchmark. A Python function that passes unit tests is an objective, verifiable signal. At A2 scale (30M params) with execution-verified code training, meaningful HumanEval scores are achievable.

-----

## CLI

```
fardrun run --program azim.fard --out <out> -- <command> [options]

generate   --prompt "..." --checkpoint <path> --mode greedy|topk|topp
inspect    --checkpoint <path>
verify     --proof <path>
eval       --checkpoints <dir>
help
```

-----

## Multi-Language Pipeline

```
Language control tokens prepended to every training record:
<|LANG_FARD|> = 4  <|LANG_PYTHON|> = 5  <|LANG_RUST|> = 6  <|LANG_JS|> = 7

Generation → Execution → Test → Accept/Reject → Train → Receipt
```

-----

## Architecture

```
d_model: 32, d_ff: 64, n_layers: 2, vocab: 600 (BPE), params: ~50,000
```

Blockwise multi-direction SPSA. All weights train simultaneously. Native linalg — 28x speedup.

-----

## Test Coverage

188 test files. 0 failures.

-----

## Repository Structure

```
packages/azim_trial/         — core LM training system
packages/azim_code/
  verifier.fard              — execution verifiers (Python, JS, Rust, FARD)
  test_harness.fard          — unit-test runner (Python, JS, Rust)
  humaneval_runner.fard      — HumanEval pass/fail with receipts
  tokenizer.fard             — 159-token multi-language tokenizer
  lang_detect.fard           — language detection
  corpus_packer.fard         — language-tagged corpus
  multilang_generation_wrapper.fard
  hybrid_proposer.fard
  hybrid_loop.fard
  scale_gate.fard
  loop_run.fard

azim.fard                    — CLI
run_benchmark.fard           — benchmark suite
main_lm.fard                 — OWT training

tests/
  test_*.fard  (188 files)
```

-----

## License

MUI