# Azim

Deterministic distributed AI training on FARD.

Azim is a training system built on deterministic execution, cryptographic receipts, replay-verifiable distributed computation, validator-supervised optimization, and lawful output constraints. Pure FARD — no Python, no external ML libraries, 12,379 lines of code.

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

Generation confirmed: shard 0 and shard 79 produce different outputs from same prompt.

Azim-Code self-training loop. 5 iterations completed.

```
Steps:   13 → 231 → 636 → 901 → 1,166 (compounding)
Records: 53 merged corpus
Gate:    PASS every iteration
```

-----

## Status

|Milestone                                             |Status|
|------------------------------------------------------|------|
|Deterministic runtime (FARD)                          |done  |
|Cryptographic receipt chain                           |done  |
|Real gradient descent (SPSA)                          |done  |
|Full OWT training run (classifier)                    |done  |
|Neural path authoritative                             |done  |
|Next-token prediction + generation                    |done  |
|linalg native ops (28x speedup)                       |done  |
|Structural tokenizer (66 tokens)                      |done  |
|BPE tokenizer (500 merges, vocab 600)                 |done  |
|Verifier-gated self-training loop                     |done  |
|Scale gate                                            |done  |
|LM run on OWT (80 shards)                             |done  |
|Architecture expansion (d_model=32, n_layers=2)       |done  |
|Blockwise SPSA — all weights simultaneously           |done  |
|Multi-direction SPSA (K directions, averaged gradient)|done  |
|Train at scale (cloud GPU)                            |next  |
|Generation evaluation suite                           |next  |

-----

## What Azim Does

Azim trains a language model on real data with a closed verifier-gated self-improvement loop. Every training step is cryptographically receipted. Every scale decision is gated on evidence.

**OWT Pipeline** — trains on real web text:

- Downloads OpenWebText parquet shards from HuggingFace
- Tokenizes with BPE or character-level vocabulary
- Trains all weights via blockwise multi-direction SPSA
- Checkpoints with receipt after each shard
- Generates text autoregressively via greedy decoding

**Azim-Code Pipeline** — trains on verified source code:

- Packs source files into tokenized training corpus
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

```
W_U_lm   600×32   19,200 params   LM head
W_Q      32×32     1,024 params   Attention query (layer 1)
W_K      32×32     1,024 params   Attention key (layer 1)
W_V      32×32     1,024 params   Attention value (layer 1)
W_O      32×32     1,024 params   Attention output (layer 1)
W_Q2     32×32     1,024 params   Attention query (layer 2)
W_K2     32×32     1,024 params   Attention key (layer 2)
W_V2     32×32     1,024 params   Attention value (layer 2)
W_O2     32×32     1,024 params   Attention output (layer 2)
W_gate   64×32     2,048 params   FFN gate (layer 1)
W_up     64×32     2,048 params   FFN up (layer 1)
W_down   32×64     2,048 params   FFN down (layer 1)
```

All weights update in a single training step. Each block gets K independent SPSA directions. Gradients are averaged across K estimates. Deterministic. Receipted.

-----

## Gradient Method

Blockwise multi-direction SPSA:

```
for each weight matrix W_i:
    for k in 1..K:
        d_k = hash-derived +/-1 direction (step, block, k)
        l+_k = NLL(state with W_i + e*d_k)
        l-_k = NLL(state with W_i - e*d_k)
        grad_k = ((l+_k - l-_k) / 2e) * d_k
    grad_i = mean(grad_1 .. grad_K)
    W_i = W_i - lr * grad_i
```

K=3 gives 3x better gradient quality at 6 forward passes per block instead of 2. All deterministic. All receipted. Native linalg ops — 28x speedup.

-----

## Tokenizers

**azim_trial/tokenizer.fard** — 129-token character-level. Used for initial training runs.

**azim_code/tokenizer.fard** — 66-token structural tokenizer. Language-agnostic. Handles keywords, operators, identifiers, literals, comments. Works on FARD, Python, JavaScript, Rust, Go. Every tokenization receipted.

**azim_trial/bpe_train.fard + bpe_encode.fard** — Learned BPE. 500 merges on real OpenWebText. 600-token vocabulary. Real English subwords: th, in, er, the, ing, and. Deterministic. Receipted manifest.

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

155 test files. 0 failures.

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
|Blockwise SPSA (all weights)   |8    |
|Multi-direction SPSA           |9    |
|Azim-Code pipeline             |9    |
|Neural authority               |6    |
|Integration + other            |311  |

-----

## Repository Structure

```
packages/azim_trial/
  tensor.fard              — native linalg ops
  linalg_bridge.fard       — float <-> linalg bytes bridge
  weights_32.fard          — d_model=32, n_layers=2, vocab=600
  block_32.fard            — 2-layer transformer forward pass
  train_all_weights.fard   — blockwise SPSA over all weight matrices
  spsa_multi.fard          — multi-direction SPSA, K gradient estimates
  bpe_train.fard           — BPE merge rule learner
  bpe_encode.fard          — BPE encoder/decoder
  generation_lm.fard       — autoregressive greedy generation
  ...

packages/azim_code/
  tokenizer.fard           — 66-token structural tokenizer
  corpus_packer.fard       — pack source files to JSONL
  generation_wrapper.fard  — generate + execute + verify
  accepted_dataset.fard    — filter to accepted corpus
  code_train_adapter.fard  — train on verified code
  retraining_manifest.fard — full audit chain document
  scale_gate.fard          — gate scale decisions on evidence
  loop_run.fard            — orchestrate full self-training loop

tests/
  test_*.fard  (155 files)

out/checkpoints/           — classifier run (80 shards)
out/lm_checkpoints2/       — LM run (80 shards)
out/bpe/                   — BPE manifest
out/weights/               — saved weight matrices
```

-----

## Running

```
fardrun test --program tests/test_spsa_multi.fard
fardrun test --program tests/test_train_all_weights.fard
fardrun test --program tests/test_block_32.fard
fardrun test --program tests/test_bpe_encode.fard
fardrun run  --program test_azim_code_loop_run.fard --out out/loop
fardrun run  --program main_lm.fard --out out/lm_full_run
```

-----

## License

MUI