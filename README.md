# Azim

Deterministic distributed AI training on FARD.

Azim is a training system built on deterministic execution, cryptographic receipts, replay-verifiable distributed computation, validator-supervised optimization, and lawful output constraints. Pure FARD — no Python, no external ML libraries, 12,885 lines of code.

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

Generation evaluation across 9 checkpoints confirmed. Outputs change across training. Semantic tokens (liquid, fire, hot, cold, combustion) emerge with top-k sampling.

Azim-Code self-training loop. 5 iterations completed.

```
Steps:   13 → 231 → 636 → 901 → 1,166 (compounding)
Records: 53 merged corpus
Gate:    PASS every iteration
```

-----

## Status

|Milestone                                                 |Status|
|----------------------------------------------------------|------|
|Deterministic runtime (FARD)                              |done  |
|Cryptographic receipt chain                               |done  |
|Real gradient descent (SPSA)                              |done  |
|Full OWT training run (classifier)                        |done  |
|Neural path authoritative                                 |done  |
|Next-token prediction + generation                        |done  |
|linalg native ops (28x speedup)                           |done  |
|Structural tokenizer (66 tokens)                          |done  |
|BPE tokenizer (500 merges, vocab 600)                     |done  |
|Verifier-gated self-training loop                         |done  |
|Scale gate                                                |done  |
|LM run on OWT (80 shards)                                 |done  |
|Architecture expansion (d_model=32, n_layers=2)           |done  |
|Blockwise SPSA — all weights simultaneously               |done  |
|Multi-direction SPSA (K directions, averaged gradient)    |done  |
|Generation evaluation suite                               |done  |
|Deterministic samplers (greedy, top-k, top-p, temperature)|done  |
|Product interface (CLI)                                   |next  |
|Train at scale (cloud GPU)                                |next  |

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

- Packs source files into tokenized training corpus (full or focused)
- Generates code candidates, executes via fardrun
- Accepts candidates that run and verify receipts
- Trains on accepted corpus only
- Full audit chain from source SHA to trained weights
- Scale gate: loss decrease + verified receipts required
- 5 iterations complete, step count compounding: 13 → 1,166

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

### Trained Parameters (Blockwise Multi-Direction SPSA)

All weight matrices update simultaneously per step. Each block gets K independent SPSA directions. Gradients averaged across K estimates.

```
W_U_lm   600×32   19,200 params   LM head
W_Q/K/V/O  32×32   1,024 each    Attention (layer 1)
W_Q2/K2/V2/O2      1,024 each    Attention (layer 2)
W_gate/up  64×32   2,048 each    FFN (layer 1)
W_down     32×64   2,048 params   FFN down (layer 1)
```

-----

## Generation Modes

**Greedy** — always picks argmax. Deterministic. Tends to collapse on dominant token.

**Top-k** — sample from k highest probability tokens. Temperature controls sharpness. Deterministic via hash-derived seed.

**Top-p (nucleus)** — sample from smallest set of tokens summing to probability p. Deterministic via hash-derived seed.

Generation evaluation across checkpoints (shard 0 vs shard 79, same prompt):

```
Shard  0: R\WeR\WeR          (random noise — untrained)
Shard 30: RSgreencolorRS     (semantic tokens emerging)
Shard 79 top-k: liquid hot combustion needs-evidence
```

-----

## Tokenizers

**azim_trial/tokenizer.fard** — 129-token character-level. Used for initial training runs.

**azim_code/tokenizer.fard** — 66-token structural tokenizer. Language-agnostic. Works on FARD, Python, JavaScript, Rust, Go. Every tokenization receipted.

**azim_trial/bpe_train.fard + bpe_encode.fard** — Learned BPE. 500 merges on real OpenWebText. 600-token vocabulary. Real English subwords: th, in, er, the, ing, and.

-----

## Receipts

Every computation emits a SHA-256 receipt over canonical JSON:

```
receipt = sha256(canonicalize({
  component: "...",
  version:   "...",
  output:    <actual computed output>
}))
```

Receipts chain across steps into a final audit proof. Replay-verifiable.

-----

## Test Coverage

164 test files. 0 failures.

|Area                            |Tests|
|--------------------------------|-----|
|Tensor core + linalg            |20   |
|Tokenizers (trial + code + BPE) |24   |
|Attention + FFN                 |10   |
|Loss + Gradients                |14   |
|RSSM (fixed + learned)          |18   |
|Distributed scan                |12   |
|Validator + backpressure        |14   |
|Receipt + audit chain           |20   |
|Training run + manifest         |18   |
|Phase contracts (6, 7, 8)       |29   |
|OWT loader + training           |8    |
|LM objective + generation       |18   |
|Architecture d_model=32         |12   |
|Blockwise + multi-direction SPSA|17   |
|Generation evaluation           |6    |
|Deterministic samplers          |9    |
|Azim-Code pipeline              |9    |
|Neural authority                |6    |
|Integration + other             |294  |

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
  ...

packages/azim_code/
  tokenizer.fard           — 66-token structural tokenizer
  corpus_packer.fard       — pack source files to JSONL
  focused_corpus_packer.fard — pack azim_trial only (higher quality)
  generation_wrapper.fard  — generate + execute + verify
  accepted_dataset.fard    — filter to accepted corpus
  code_train_adapter.fard  — train on verified code
  retraining_manifest.fard — full audit chain document
  scale_gate.fard          — gate scale decisions on evidence
  loop_run.fard            — orchestrate full self-training loop

tests/
  test_*.fard  (164 files)

out/checkpoints/           — classifier run (80 shards)
out/lm_checkpoints2/       — LM run (80 shards)
out/bpe/                   — BPE manifest
out/eval/                  — generation evaluation results
```

-----

## Running

```
fardrun test --program tests/test_samplers.fard
fardrun test --program tests/test_generation_eval.fard
fardrun test --program tests/test_train_all_weights.fard
fardrun test --program tests/test_spsa_multi.fard
fardrun run  --program run_generation_eval.fard --out out/eval
fardrun run  --program test_azim_code_loop_run.fard --out out/loop
fardrun run  --program main_lm.fard --out out/lm_full_run
```

-----

## License

MUI