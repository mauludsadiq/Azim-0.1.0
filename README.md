# Azim

Deterministic distributed AI training on FARD.

Azim is a training system built on deterministic execution, cryptographic receipts, replay-verifiable distributed computation, validator-supervised optimization, and lawful output constraints. Pure FARD — no Python, no external ML libraries, 11,988 lines of code.

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

LM objective run (next-token prediction, 129-token vocab). All 80 shards complete.

```
Mean loss:    4.7927  (below random baseline 4.8598)
Final loss:   4.1237  (-0.74 vs random)
Below random: 47/80 shards
Trend slope:  -0.0137/shard
L2 stable:    18.41 - 18.93
```

Generation confirmed: shard 0 and shard 79 produce different outputs from same prompt.

-----

## Status

|Milestone                                                 |Status |
|----------------------------------------------------------|-------|
|Deterministic runtime                                     |done   |
|Cryptographic receipt chain                               |done   |
|Real gradient descent (SPSA)                              |done   |
|Full OWT training run (classifier)                        |done   |
|Neural path authoritative                                 |done   |
|Next-token prediction objective                           |done   |
|Autoregressive generation                                 |done   |
|linalg native ops (28x speedup)                           |done   |
|Structural tokenizer (language-agnostic, 66 tokens)       |done   |
|BPE tokenizer (500 merges, vocab 600)                     |done   |
|Verifier-gated self-training loop                         |done   |
|Scale gate                                                |done   |
|LM run on OWT (129-token vocab)                           |done   |
|Architecture expansion (d_model=32, n_layers=2, vocab=600)|running|
|Train all weights (embeddings, attention, FFN)            |next   |
|Multi-direction SPSA                                      |next   |

-----

## What Azim Does

Azim trains a language model on real data with a closed verifier-gated self-improvement loop.

Two training pipelines:

**OWT Pipeline** — trains on real web text:

- Downloads OpenWebText parquet shards from HuggingFace
- Tokenizes with BPE or character-level vocabulary
- Trains via SPSA gradient descent
- Checkpoints with receipt after each shard
- Generates text autoregressively via greedy decoding

**Azim-Code Pipeline** — trains on verified source code:

- Packs source files into tokenized training corpus
- Generates code candidates
- Executes each candidate via fardrun — real execution, not simulation
- Accepts candidates that run and verify
- Trains on accepted corpus only
- Produces retraining manifest with full cryptographic audit chain
- Gates scale decisions on measured loss decrease + verified receipts

Loop run results:

```
accepted:    3/3 candidates
loss delta:  -0.0092
steps:       231
records:     28
gate:        PASS
```

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

### Previous Model (d_model=8)

```
d_model:    8
d_ff:       16
n_layers:   1
vocab_size: 129 (character)
params:     ~3,000
```

### Transformer Stack

|Phase|Description                                                               |
|-----|--------------------------------------------------------------------------|
|0    |Deterministic Runtime (FARD)                                              |
|1    |Aware-Tower — semantic realization with lawful output constraints         |
|2    |RSSM + Associative Scan — learned state evolution, distributed prefix scan|
|3    |Gradient Oracle — SPSA gradients over real NLL loss                       |
|4    |Dual-Receipt Protocol — math and impl receipts independently auditable    |
|5    |Dynamic Basis Expansion — cosine similarity monitoring, expansion events  |
|6    |Distributed Training — three-node cluster with real RSSM train steps      |
|7    |Async Validator — leakage probe, tower independence, backpressure control |
|8    |Full Run + Audit Proof — end-to-end receipt chain with final proof        |
|Code |Verifier-gated self-training on source code                               |

-----

## Tokenizers

**azim_trial/tokenizer.fard** — 129-token character-level vocabulary. Used for initial training runs.

**azim_code/tokenizer.fard** — 66-token structural tokenizer. Language-agnostic. Handles keywords, operators, identifiers, literals, comments. Works on any C-like syntax: FARD, Python, JavaScript, Rust, Go. Every tokenization receipted.

**azim_trial/bpe_train.fard + bpe_encode.fard** — Learned BPE tokenizer. 500 merges trained on real OpenWebText. Vocabulary of 600 subword tokens. Produces real English subwords: `th`, `in`, `er`, `the`, `ing`, `and`. Encoder applies merge rules greedily. Deterministic. Receipted manifest.

-----

## Verifier-Gated Self-Training

Azim trains on its own verified outputs:

```
pack source files -> tokenized corpus (structural tokenizer)
generate code candidates
execute each candidate via fardrun
accept if execution succeeds + receipt verifies
train W_U_lm on accepted corpus only
produce retraining manifest (full audit chain)
scale gate: require loss decrease + N accepted + all receipts
```

Scale gate checks:

```
loss_decreased:  true
accepted_ok:     true
records_ok:      true
receipts_ok:     true
decision:        PASS
```

-----

## Gradient Method

SPSA with rotating direction:

```
d = hash-derived +/-1 direction (from W state + step index)
l_plus  = NLL(W + e*d, tokens, pos)
l_minus = NLL(W - e*d, tokens, pos)
grad    = ((l_plus - l_minus) / 2e) * d
W       = W - lr * grad
```

3 forward passes per step. Native linalg ops — 28x speedup over interpreted tensor ops.

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

Receipts chain across steps into a final audit proof.

-----

## Test Coverage

151 test files. 0 failures.

|Area                           |Tests|
|-------------------------------|-----|
|Tensor core + linalg           |20   |
|Tokenizers (trial + code + BPE)|24   |
|Attention + FFN                |10   |
|Loss + Gradients               |14   |
|RSSM (fixed + learned)         |18   |
|Distributed scan               |12   |
|Validator + backpressure       |14   |
|Receipt + audit chain          |20   |
|Training run + manifest        |18   |
|Phase contracts (6, 7, 8)      |29   |
|OWT loader + training          |8    |
|LM objective + generation      |13   |
|Architecture d_model=32        |12   |
|Azim-Code pipeline             |9    |
|Neural authority               |6    |
|Integration + other            |324  |

-----

## Repository Structure

```
packages/azim_trial/       — core LM training system
  tensor.fard              — native linalg ops
  linalg_bridge.fard       — float <-> linalg bytes bridge
  weights.fard             — d_model=8 weights
  weights_32.fard          — d_model=32, n_layers=2, vocab=600
  block_32.fard            — 2-layer transformer forward pass
  lm_head.fard             — 129-token LM head
  lm_train.fard            — SPSA training (d_model=8)
  lm_train_32.fard         — SPSA training (d_model=32)
  lm_owt_train.fard        — OWT streaming pipeline
  bpe_train.fard           — BPE merge rule learner
  bpe_encode.fard          — BPE encoder/decoder
  generation_lm.fard       — autoregressive greedy generation
  ...

packages/azim_code/        — verifier-gated self-training
  tokenizer.fard           — 66-token structural tokenizer (language-agnostic)
  corpus_packer.fard       — pack source files to JSONL
  generation_wrapper.fard  — generate + execute + verify candidates
  accepted_dataset.fard    — filter to accepted corpus
  code_train_adapter.fard  — train on verified code
  retraining_manifest.fard — full audit chain document
  scale_gate.fard          — gate scale decisions on evidence
  loop_run.fard            — orchestrate full self-training loop

tests/
  test_*.fard  (151 files)

out/checkpoints/           — classifier run (80 shards)
out/lm_checkpoints2/       — LM run (80 shards complete)
out/bpe/                   — BPE manifest (500 merges, vocab 600)
out/weights/               — saved weight matrices
```

-----

## Running

```
fardrun test --program tests/test_lm_objective.fard
fardrun test --program tests/test_block_32.fard
fardrun test --program tests/test_bpe_encode.fard
fardrun run  --program main_lm.fard --out out/lm_full_run
fardrun run  --program test_azim_code_loop_run.fard --out out/loop
fardrun run  --program main.fard --out out/main_run
```

-----

## License

MUI