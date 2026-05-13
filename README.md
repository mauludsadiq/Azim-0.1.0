# Azim

Deterministic distributed AI training on FARD.

Azim is a training system built on deterministic execution, cryptographic receipts, replay-verifiable distributed computation, validator-supervised optimization, and lawful output constraints. Pure FARD — no Python, no external ML libraries, 13,606 lines of code.

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
Languages: FARD, Python, Rust, JavaScript
Gate:    PASS every iteration
```

-----

## Status

|Milestone                                         |Status|
|--------------------------------------------------|------|
|Deterministic runtime (FARD)                      |done  |
|Cryptographic receipt chain                       |done  |
|Real gradient descent (SPSA)                      |done  |
|Full OWT training run (classifier)                |done  |
|Neural path authoritative                         |done  |
|Next-token prediction + generation                |done  |
|linalg native ops (28x speedup)                   |done  |
|Multi-language structural tokenizer (155 tokens)  |done  |
|BPE tokenizer (500 merges, vocab 600)             |done  |
|Verifier-gated self-training loop                 |done  |
|Scale gate                                        |done  |
|LM run on OWT (80 shards)                         |done  |
|Architecture expansion (d_model=32, n_layers=2)   |done  |
|Blockwise SPSA — all weights simultaneously       |done  |
|Multi-direction SPSA                              |done  |
|Generation evaluation suite                       |done  |
|Deterministic samplers (greedy, top-k, top-p)     |done  |
|Product interface (CLI)                           |done  |
|Public benchmark pack                             |done  |
|Multi-language verifier (Python, Rust, JS, FARD)  |done  |
|Hybrid orchestration (LLM proposes, Azim verifies)|done  |
|Train at scale (cloud GPU)                        |next  |

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

## Hybrid Orchestration

Azim uses external LLMs as proposal engines while holding authority over execution, verification, and training.

```
external LLM proposes code (Python, Rust, JavaScript, FARD)
Azim writes candidate to disk
Azim executes via real compiler (python3, rustc, node, fardrun)
Azim verifies execution receipt
Azim accepts or rejects
Azim trains on accepted corpus
full receipt chain covers every step
```

The LLM is a proposal engine. Azim is the authority. Every accepted candidate is cryptographically receipted from proposal to training.

-----

## Multi-Language Verifier

```
FARD:       fardrun run   — executes and verifies receipts
Python:     python3 -m py_compile   — syntax check
Rust:       rustc --edition=2021 --crate-type=lib   — compile check
JavaScript: node --check   — syntax check
```

All three languages confirmed: `accepted: true`, receipts at every step.

-----

## Tokenizers

**azim_code/tokenizer.fard v2.0.0** — 155-token structural tokenizer. Language-agnostic.

- **FARD**: let, fn, if, then, else, import, export, match…
- **Python**: def, class, lambda, yield, async, await, except, None, True, False…
- **Rust**: struct, enum, impl, trait, mut, pub, crate, unsafe, dyn…
- **JavaScript**: const, var, function, typeof, instanceof, async, await…
- **All**: operators, identifiers, integers, floats, strings, comments, whitespace

**azim_trial/bpe_train.fard + bpe_encode.fard** — Learned BPE. 500 merges. 600-token vocabulary. Real English subwords: th, in, er, the, ing, and.

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

### Trained Parameters (Blockwise Multi-Direction SPSA)

All weight matrices update simultaneously per step. K independent SPSA directions per block. Gradients averaged.

```
W_U_lm   600×32   LM head
W_Q/K/V/O  32×32  Attention (layer 1 + layer 2)
W_gate/up/down     FFN (layer 1 + layer 2)
```

### Gradient Method

```
for each weight matrix W_i:
    for k in 1..K:
        d_k = hash-derived +/-1 direction
        grad_k = SPSA estimate
    grad_i = mean(grad_1 .. grad_K)
    W_i = W_i - lr * grad_i
```

Native linalg ops — 28x speedup. All deterministic. All receipted.

-----

## Benchmark

```
fardrun run --program run_benchmark.fard --out out/benchmark

determinism:  PASS  (same checkpoint + prompt = same output)
receipt:      PASS  (SHA-256 receipt present and valid)
diversity:    PASS  (top-k generates diverse outputs)
integrity:    PASS  (checkpoint dims/data/loss valid)
```

Reproducible on any machine with fardrun.

-----

## Receipts

Every computation emits a SHA-256 receipt over canonical JSON. Receipts chain across steps into a final audit proof. Replay-verifiable.

-----

## Test Coverage

175 test files. 0 failures.

-----

## Repository Structure

```
packages/azim_trial/
  tensor.fard              — native linalg ops
  linalg_bridge.fard       — float <-> linalg bytes bridge
  weights_32.fard          — d_model=32, n_layers=2, vocab=600
  block_32.fard            — 2-layer transformer
  train_all_weights.fard   — blockwise SPSA all weights
  spsa_multi.fard          — multi-direction SPSA
  samplers.fard            — greedy, top-k, top-p
  generation_v2.fard       — generation with sampling modes
  generation_eval.fard     — checkpoint evaluation
  benchmark.fard           — public benchmark suite
  bpe_train.fard           — BPE trainer
  bpe_encode.fard          — BPE encoder/decoder

packages/azim_code/
  tokenizer.fard           — 155-token multi-language tokenizer
  lang_detect.fard         — language detection
  corpus_packer.fard       — multi-language corpus with lang tags
  verifier.fard            — multi-language execution verifier
  hybrid_proposer.fard     — LLM proposal + verification
  hybrid_loop.fard         — full hybrid training loop
  generation_wrapper.fard  — generate + verify candidates
  accepted_dataset.fard    — filter to accepted corpus
  code_train_adapter.fard  — train on verified code
  retraining_manifest.fard — full audit chain
  scale_gate.fard          — evidence-gated scaling
  loop_run.fard            — full self-training loop

azim.fard                  — CLI entrypoint
run_benchmark.fard         — benchmark suite
main_lm.fard               — OWT training

tests/
  test_*.fard  (175 files)

out/checkpoints/           — classifier run (80 shards)
out/lm_checkpoints2/       — LM run (80 shards)
out/bpe/                   — BPE manifest
out/eval/                  — generation evaluation
out/benchmark/             — benchmark results
```

-----

## License

MUI