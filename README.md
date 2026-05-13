# Azim

Deterministic distributed AI training on FARD.

Azim is a training system built on deterministic execution, cryptographic receipts, replay-verifiable distributed computation, validator-supervised optimization, and lawful output constraints. Pure FARD — no Python, no external ML libraries, 13,401 lines of code.

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
Trend slope:  -0.0137/shard
```

Benchmark suite: 4/4 passing (determinism, receipt, diversity, integrity).

Azim-Code self-training loop. 5 iterations completed.

```
Steps:   13 → 231 → 636 → 901 → 1,166 (compounding)
Records: 53 merged corpus
Gate:    PASS every iteration
```

-----

## Status

|Milestone                                       |Status|
|------------------------------------------------|------|
|Deterministic runtime (FARD)                    |done  |
|Cryptographic receipt chain                     |done  |
|Real gradient descent (SPSA)                    |done  |
|Full OWT training run (classifier)              |done  |
|Neural path authoritative                       |done  |
|Next-token prediction + generation              |done  |
|linalg native ops (28x speedup)                 |done  |
|Multi-language structural tokenizer (155 tokens)|done  |
|BPE tokenizer (500 merges, vocab 600)           |done  |
|Verifier-gated self-training loop               |done  |
|Scale gate                                      |done  |
|LM run on OWT (80 shards)                       |done  |
|Architecture expansion (d_model=32, n_layers=2) |done  |
|Blockwise SPSA — all weights simultaneously     |done  |
|Multi-direction SPSA                            |done  |
|Generation evaluation suite                     |done  |
|Deterministic samplers (greedy, top-k, top-p)   |done  |
|Product interface (CLI)                         |done  |
|Public benchmark pack                           |done  |
|Multi-language verifier (Python, Rust, JS, FARD)|done  |
|Train at scale (cloud GPU)                      |next  |
|Hybrid orchestration                            |next  |

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

## Multi-Language Verifier

Azim verifies code candidates in any language using the actual compiler or interpreter:

```
FARD:       fardrun run   — executes and verifies receipts
Python:     python3 -m py_compile   — syntax check
Rust:       rustc --edition=2021 --crate-type=lib   — compile check
JavaScript: node --check   — syntax check
```

Each verification produces a SHA-256 receipt over the execution result. The full chain — source SHA → execution → receipt — is preserved for every candidate in every language.

-----

## Tokenizers

**azim_code/tokenizer.fard v2.0.0** — 155-token structural tokenizer. Language-agnostic.

- **FARD**: let, fn, if, then, else, import, export, match…
- **Python**: def, class, lambda, yield, async, await, except, finally, None, True, False…
- **Rust**: struct, enum, impl, trait, mut, pub, crate, unsafe, dyn, loop…
- **JavaScript**: const, var, function, typeof, instanceof, async, await, of…
- **All**: operators, identifiers, integers, floats, strings, comments (// # /* */), whitespace

Every tokenization receipted. Language detected from file extension. Tagged in corpus records.

**azim_trial/bpe_train.fard + bpe_encode.fard** — Learned BPE. 500 merges. 600-token vocabulary.

-----

## Architecture

### Current Model (d_model=32)

```
d_model:    32
d_ff:       64
n_layers:   2
vocab_size: 600 (BPE)
params:     ~50,000
```

### Gradient Method

Blockwise multi-direction SPSA. K directions per weight matrix. Gradients averaged. All deterministic. All receipted. Native linalg — 28x speedup.

-----

## Benchmark

```
fardrun run --program run_benchmark.fard --out out/benchmark

determinism:  PASS
receipt:      PASS
diversity:    PASS
integrity:    PASS
```

-----

## Test Coverage

172 test files. 0 failures.

-----

## Repository Structure

```
packages/azim_trial/         — core LM training system
  tensor.fard                — native linalg ops
  linalg_bridge.fard         — float <-> linalg bytes bridge
  weights_32.fard            — d_model=32, n_layers=2, vocab=600
  block_32.fard              — 2-layer transformer
  train_all_weights.fard     — blockwise SPSA all weights
  spsa_multi.fard            — multi-direction SPSA
  samplers.fard              — greedy, top-k, top-p
  generation_v2.fard         — generation with sampling modes
  generation_eval.fard       — checkpoint evaluation
  benchmark.fard             — public benchmark suite
  bpe_train.fard             — BPE trainer
  bpe_encode.fard            — BPE encoder/decoder

packages/azim_code/          — verifier-gated self-training
  tokenizer.fard             — 155-token multi-language tokenizer
  lang_detect.fard           — language detection
  corpus_packer.fard         — multi-language corpus with lang tags
  verifier.fard              — multi-language execution verifier
  generation_wrapper.fard    — generate + verify candidates
  accepted_dataset.fard      — filter to accepted corpus
  code_train_adapter.fard    — train on verified code
  retraining_manifest.fard   — full audit chain
  scale_gate.fard            — evidence-gated scaling
  loop_run.fard              — full self-training loop

azim.fard                    — CLI entrypoint
run_benchmark.fard           — benchmark suite
main_lm.fard                 — OWT training

tests/
  test_*.fard  (172 files)
```

-----

## License

MUI