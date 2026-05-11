# Azim

Deterministic distributed AI training on FARD.

Azim is a training system built on deterministic execution, cryptographic receipts, replay-verifiable distributed computation, validator-supervised optimization, and lawful output constraints. Pure FARD — no Python, no external ML libraries, 9,043 lines of code.

-----

## Training Results

Full OpenWebText run. All 80 shards. 15 hours. MacBook Pro. Pure FARD.

```
Shard  0:  0.7605
Shard 10:  0.1883
Shard 20:  0.0981
Shard 30:  0.0660
Shard 40:  0.0491
Shard 50:  0.0392
Shard 60:  0.0327
Shard 70:  0.0281
Shard 79:  0.0244
```

96.8% loss reduction. Every step cryptographically receipted. Audit proof complete.

LM objective run in progress — next-token prediction over full vocabulary.

-----

## Status

|Milestone                         |Status |
|----------------------------------|-------|
|Deterministic runtime             |done   |
|Cryptographic receipt chain       |done   |
|Real gradient descent (SPSA)      |done   |
|Full OWT training run (classifier)|done   |
|Neural path authoritative         |done   |
|Next-token prediction objective   |done   |
|Autoregressive generation         |done   |
|LM training on OWT                |running|
|BPE tokenizer                     |next   |
|Larger d_model / more layers      |next   |

-----

## What Azim Does

Azim trains a language model on real data. The neural path is authoritative — the model’s logits determine output, not a hardcoded lookup. It downloads OpenWebText shards, runs next-token prediction, receipts every step, and streams through the full dataset.

The training pipeline:

- Downloads OpenWebText parquet shards from HuggingFace
- Extracts real web text via strings extraction and quality filtering
- Tokenizes with a fixed greedy vocabulary (129 tokens)
- Embeds tokens into distinct 8-dimensional vectors per token ID
- Runs a transformer block: RMS norm, attention, FFN, residual
- Computes per-position hidden states
- Projects to vocab_size (129) logits via W_U_lm
- Computes NLL loss over next-token targets
- Updates W_U_lm via SPSA gradient descent
- Generates text autoregressively via greedy decoding
- Chains SHA-256 receipts over every computed output
- Checkpoints W_U_lm with receipt after each shard

-----

## Architecture

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

-----

## LM Objective

Next-token prediction over the full vocabulary:

```
for each position pos in token_ids[0..n-1]:
    hidden = rms_norm(block(embed(token_ids[0..pos])))
    logits = W_U_lm . hidden          # shape: vocab_size x 1
    loss   = NLL(logits, token_ids[pos+1])

grad = SPSA(loss, W_U_lm)
W_U_lm = W_U_lm - lr * grad
```

W_U_lm is 129x8 — projects 8-dimensional hidden state to 129-token vocabulary.

-----

## Autoregressive Generation

```
prompt_ids = tokenize(prompt)
while steps < max_new_tokens:
    hidden = block(embed(prompt_ids))
    logits = W_U_lm . hidden
    next_id = argmax(logits)
    if next_id == EOS: stop
    prompt_ids = append(prompt_ids, next_id)
```

Greedy decoding. Deterministic. Receipted.

-----

## Gradient Method

SPSA with fixed direction vector:

```
d = fixed +/-1 direction (precomputed from hash, stable across steps)
l_plus  = NLL(W + e*d, tokens, pos)
l_minus = NLL(W - e*d, tokens, pos)
grad    = ((l_plus - l_minus) / 2e) * d
W       = W - lr * grad
```

3 forward passes per step regardless of parameter count.

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

98 test files. 0 failures.

|Area                     |Tests|
|-------------------------|-----|
|Tensor core              |14   |
|Tokenizer                |9    |
|Attention + FFN          |10   |
|Loss + Gradients         |14   |
|RSSM (fixed + learned)   |18   |
|Distributed scan         |12   |
|Validator + backpressure |14   |
|Receipt + audit chain    |20   |
|Training run + manifest  |18   |
|Phase contracts (6, 7, 8)|29   |
|OWT loader + training    |8    |
|LM objective + generation|13   |
|Neural authority         |6    |
|Integration + other      |303  |

-----

## Repository Structure

```
packages/azim_trial/
  tensor.fard
  weights.fard
  embedding.fard
  attention.fard
  block.fard
  loss.fard
  lm_head.fard
  lm_train.fard
  lm_owt_train.fard
  generation_lm.fard
  train_step.fard
  rssm.fard
  distributed_scan.fard
  cluster_run_1p5b.fard
  async_validator.fard
  owt_loader.fard
  owt_train.fard
  owt_checkpoint.fard
  owt_full_run.fard
  openwebtext_full_run.fard
  final_audit_proof.fard
  ...

tests/
  test_*.fard  (98 files)

out/checkpoints/
  shard_0.json .. shard_79.json

out/lm_checkpoints/
  shard_*.json  (LM objective run)
```

-----

## Running

```
fardrun test --program tests/test_lm_objective.fard
fardrun test --program tests/test_generation_lm.fard
fardrun test --program tests/test_neural_authority.fard
fardrun run  --program main_lm.fard --out out/lm_full_run
fardrun run  --program main.fard --out out/main_run
```

-----

## License

MUI