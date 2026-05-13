# Azim

Deterministic distributed AI training on FARD.

Azim is a training system built on deterministic execution, cryptographic receipts, replay-verifiable distributed computation, validator-supervised optimization, and lawful output constraints. Pure FARD — no Python, no external ML libraries, 13,907 lines of code.

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

Multi-language self-training loop. Full pipeline confirmed.

```
Languages:    FARD, Python, Rust, JavaScript
Accepted:     4/4 candidates (one per language)
Verified via: fardrun, python3, rustc, node
Control tokens: <|LANG_FARD|> <|LANG_PYTHON|> <|LANG_RUST|> <|LANG_JS|>
Scale gate:   language diversity required
```

-----

## Status — All 18 Phases Complete

|Milestone                                         |Status|
|--------------------------------------------------|------|
|Deterministic runtime (FARD)                      |done  |
|Cryptographic receipt chain                       |done  |
|Real gradient descent (SPSA)                      |done  |
|Full OWT training run (classifier)                |done  |
|Neural path authoritative                         |done  |
|Next-token prediction + generation                |done  |
|linalg native ops (28x speedup)                   |done  |
|Multi-language structural tokenizer (159 tokens)  |done  |
|BPE tokenizer (500 merges, vocab 600)             |done  |
|Verifier-gated self-training loop                 |done  |
|Scale gate with language diversity                |done  |
|LM run on OWT (80 shards)                         |done  |
|Architecture expansion (d_model=32, n_layers=2)   |done  |
|Blockwise SPSA — all weights simultaneously       |done  |
|Multi-direction SPSA                              |done  |
|Generation evaluation suite                       |done  |
|Deterministic samplers (greedy, top-k, top-p)     |done  |
|Product interface (CLI)                           |done  |
|Public benchmark pack                             |done  |
|Multi-language verifier (Python, Rust, JS, FARD)  |done  |
|Language control tokens                           |done  |
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

## Multi-Language Pipeline

Full cycle confirmed — generate, verify, train, receipt — in all four languages:

```
FARD:       fardrun run        — executes + verifies receipts
Python:     python3 -m py_compile — syntax check
Rust:       rustc --edition=2021  — compile check
JavaScript: node --check          — syntax check
```

Each candidate is written, executed, receipted, accepted or rejected. Accepted candidates enter the training corpus with language control token prepended.

Language control tokens in the structural tokenizer:

```
<|LANG_FARD|>       id = 4
<|LANG_PYTHON|>     id = 5
<|LANG_RUST|>       id = 6
<|LANG_JS|>         id = 7
```

Every tokenized record begins with the appropriate control token. The model learns language-conditional generation.

-----

## Hybrid Orchestration

External LLMs serve as proposal engines. Azim holds authority over execution, verification, and training.

```
external LLM proposes code in any language
Azim writes candidate to disk
Azim executes via real compiler
Azim verifies receipt
Azim accepts or rejects
Azim trains on accepted corpus
full receipt chain covers every step
```

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

Blockwise multi-direction SPSA. K directions per weight matrix per step. Gradients averaged. All deterministic. All receipted. Native linalg — 28x speedup.

-----

## Tokenizers

**azim_code/tokenizer.fard v2.1.0** — 159-token structural tokenizer.

- Language control tokens: FARD, Python, Rust, JavaScript
- Keywords for all four languages
- Operators, identifiers, integers, floats, strings, comments
- Every tokenization receipted

**azim_trial/bpe_train.fard + bpe_encode.fard** — Learned BPE. 500 merges. 600-token vocabulary.

-----

## Scale Gate

Enforces evidence before any architecture expansion:

```
loss decreased:       required
min accepted:         configurable
min records:          configurable
min languages:        required (diversity enforcement)
all receipts valid:   required
```

All four checks must pass. Decision is cryptographically receipted.

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

180 test files. 0 failures.

-----

## Repository Structure

```
packages/azim_trial/
  tensor.fard, linalg_bridge.fard
  weights_32.fard, block_32.fard
  train_all_weights.fard, spsa_multi.fard
  samplers.fard, generation_v2.fard
  generation_eval.fard, benchmark.fard
  bpe_train.fard, bpe_encode.fard

packages/azim_code/
  tokenizer.fard           — 159-token multi-language tokenizer
  lang_detect.fard         — language detection from extension
  corpus_packer.fard       — language-tagged corpus with control tokens
  verifier.fard            — multi-language execution verifier
  multilang_generation_wrapper.fard — language-aware generation
  hybrid_proposer.fard     — LLM proposal + verification
  hybrid_loop.fard         — full hybrid training loop
  scale_gate.fard          — evidence + diversity gated scaling
  loop_run.fard            — full self-training loop

azim.fard                  — CLI entrypoint
run_benchmark.fard         — benchmark suite
main_lm.fard               — OWT training

tests/
  test_*.fard  (180 files)
```

-----

## License

MUI