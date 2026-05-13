# Azim

Deterministic distributed AI training on FARD.

Azim is a training system built on deterministic execution, cryptographic receipts, replay-verifiable distributed computation, validator-supervised optimization, and lawful output constraints. Pure FARD — no Python, no external ML libraries, 13,014 lines of code.

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

Azim-Code self-training loop. 5 iterations completed.

```
Steps:   13 → 231 → 636 → 901 → 1,166 (compounding)
Records: 53 merged corpus
Gate:    PASS every iteration
```

-----

## Status

|Milestone                                      |Status|
|-----------------------------------------------|------|
|Deterministic runtime (FARD)                   |done  |
|Cryptographic receipt chain                    |done  |
|Real gradient descent (SPSA)                   |done  |
|Full OWT training run (classifier)             |done  |
|Neural path authoritative                      |done  |
|Next-token prediction + generation             |done  |
|linalg native ops (28x speedup)                |done  |
|Structural tokenizer (66 tokens)               |done  |
|BPE tokenizer (500 merges, vocab 600)          |done  |
|Verifier-gated self-training loop              |done  |
|Scale gate                                     |done  |
|LM run on OWT (80 shards)                      |done  |
|Architecture expansion (d_model=32, n_layers=2)|done  |
|Blockwise SPSA — all weights simultaneously    |done  |
|Multi-direction SPSA                           |done  |
|Generation evaluation suite                    |done  |
|Deterministic samplers (greedy, top-k, top-p)  |done  |
|Product interface (CLI)                        |done  |
|Public benchmark pack                          |next  |
|Train at scale (cloud GPU)                     |next  |

-----

## CLI

```
fardrun run --program azim.fard --out <out> -- <command> [options]

generate   Generate text
           --prompt "the sky is"
           --checkpoint out/lm_checkpoints2/shard_79.json
           --mode greedy|topk|topp

inspect    Inspect a checkpoint
           --checkpoint out/lm_checkpoints2/shard_79.json

verify     Verify a checkpoint receipt
           --proof out/lm_checkpoints2/shard_79.json

eval       Evaluate generation across checkpoints
           --checkpoints out/lm_checkpoints2

help       Show usage
```

Example:

```
fardrun run --program azim.fard --out out/gen -- generate --prompt "the sky is" --mode topk
# output: .|JIrliquid@77lIIIOneeds-evidence
# receipt: sha256:16e6beb2...
```

-----

## What Azim Does

Azim trains a language model on real data with a closed verifier-gated self-improvement loop. Every training step is cryptographically receipted. Every scale decision is gated on evidence.

**OWT Pipeline** — trains on real web text:

- Downloads OpenWebText parquet shards from HuggingFace
- Tokenizes with BPE or character-level vocabulary
- Trains all weights via blockwise multi-direction SPSA
- Checkpoints with receipt after each shard
- Generates text via greedy, top-k, or top-p sampling

**Azim-Code Pipeline** — trains on verified source code:

- Packs source files into tokenized training corpus
- Generates code candidates, executes via fardrun
- Accepts candidates that run and verify receipts
- Trains on accepted corpus only
- Full audit chain from source SHA to trained weights
- Scale gate: loss decrease + verified receipts required

-----

## Architecture

### Current Model (d_model=32)

```
d_model:    32
d_ff:       64
n_layers:   2
vocab_size: 600 (BPE)
max_seq:    128
heads:      4
params:     ~50,000
```

### Gradient Method

Blockwise multi-direction SPSA. K directions per weight matrix per step. Gradients averaged across K estimates. All deterministic. All receipted. Native linalg — 28x speedup.

-----

## Tokenizers

**azim_trial/tokenizer.fard** — 129-token character-level.

**azim_code/tokenizer.fard** — 66-token structural tokenizer. Language-agnostic. Works on FARD, Python, JavaScript, Rust, Go.

**azim_trial/bpe_train.fard + bpe_encode.fard** — Learned BPE. 500 merges. 600-token vocabulary. Real English subwords.

-----

## Receipts

Every computation emits a SHA-256 receipt over canonical JSON. Receipts chain across steps into a final audit proof. Replay-verifiable.

-----

## Test Coverage

165 test files. 0 failures.

-----

## Repository Structure

```
packages/azim_trial/
  tensor.fard              — native linalg ops
  linalg_bridge.fard       — float <-> linalg bytes bridge
  weights_32.fard          — d_model=32, n_layers=2, vocab=600
  block_32.fard            — 2-layer transformer forward pass
  train_all_weights.fard   — blockwise SPSA all weight matrices
  spsa_multi.fard          — multi-direction SPSA
  samplers.fard            — greedy, top-k, top-p, temperature
  generation_v2.fard       — generation with all sampling modes
  generation_eval.fard     — evaluation across checkpoints
  bpe_train.fard           — BPE merge rule learner
  bpe_encode.fard          — BPE encoder/decoder

packages/azim_code/
  tokenizer.fard           — 66-token structural tokenizer
  corpus_packer.fard       — pack source files to JSONL
  focused_corpus_packer.fard — pack azim_trial only
  generation_wrapper.fard  — generate + execute + verify
  accepted_dataset.fard    — filter to accepted corpus
  code_train_adapter.fard  — train on verified code
  retraining_manifest.fard — full audit chain document
  scale_gate.fard          — gate scale decisions on evidence
  loop_run.fard            — orchestrate full self-training loop

azim.fard                  — CLI entrypoint
main_lm.fard               — OWT training run entrypoint

tests/
  test_*.fard  (165 files)

out/checkpoints/           — classifier run (80 shards)
out/lm_checkpoints2/       — LM run (80 shards)
out/bpe/                   — BPE manifest
out/eval/                  — generation evaluation results
```

-----

## License

MUI