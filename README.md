# Azim

Deterministic distributed AI training on FARD.

Azim is a training system built on deterministic execution, cryptographic receipts, replay-verifiable distributed computation, validator-supervised optimization, and lawful output constraints. Pure FARD — no Python, no external ML libraries, 8,560 lines of code.

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

Checkpoints for all 80 shards are in out/checkpoints/.

-----

## What Azim Does

Azim trains a neural model on real data. It downloads OpenWebText shards from HuggingFace, extracts text, runs gradient descent, receipts every step, checkpoints between shards, and streams through the full 80-shard dataset.

The training pipeline:

- Downloads OpenWebText parquet shards from HuggingFace
- Extracts real web text via strings extraction and quality filtering
- Truncates documents to 120 characters for tokenization efficiency
- Tokenizes input text with a fixed greedy vocabulary
- Embeds tokens into distinct 8-dimensional vectors per token ID
- Runs a transformer block: RMS norm, attention, FFN, residual
- Computes NLL loss over three-class label logits
- Computes SPSA gradient over W_U — 2 forward passes per step
- Updates W_U via SGD with verified loss decrease per step
- Checkpoints W_U with receipt after each shard
- Trains RSSM transition matrices with convergence verification
- Distributes training across nodes with prefix-chained associative scan
- Supervises with real leakage detection and tower independence probes
- Chains SHA-256 receipts over every computed output
- Deletes each shard after training to manage disk

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

## Gradient Method

Azim uses SPSA (Simultaneous Perturbation Stochastic Approximation) for W_U:

```
d = deterministic +/-1 direction (from weight state hash)
l_plus  = NLL(W_U + e*d, hidden, label)
l_minus = NLL(W_U - e*d, hidden, label)
grad    = ((l_plus - l_minus) / 2e) * d
W_U     = W_U - lr * grad
```

2 forward passes per step. Deterministic direction from weight state.

The RSSM trains W_h against a target state:

```
s_{t+1} = relu(W_h . s_t + W_x . x_t)
loss    = ||s_T - target||^2
W_h     = W_h - lr * finite_diff_grad
```

-----

## Shard Streaming

```
for shard_index in 0..79:
    curl shard from HuggingFace -> out/
    strings extraction + quality filter
    truncate to 120 chars
    train W_U on up to 50 documents
    checkpoint W_U + receipt to out/checkpoints/
    delete shard parquet
```

80 shards. ~11 minutes per shard. 15 hours total.

-----

## Distributed Scan

Three nodes chain state across partitions:

```
node-1: s_0 -> s_1 = transition(batch[0], s_0)
node-2: s_1 -> s_2 = transition(batch[1], s_1)
node-3: s_2 -> s_3 = transition(batch[2], s_2)
```

s_3 is bit-identical to sequential execution. Verified by test.

-----

## Validator

Three real probes run every 1000 steps:

|Probe       |Method                             |
|------------|-----------------------------------|
|Leakage     |RSSM/Tower bridge score comparison |
|Independence|Tower layer zeroing stability check|
|Receipt     |SHA-256 prefix verification        |

Backpressure: ok continues, warning adjusts, emergency pauses.

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

88 test files. 0 failures.

|Area                     |Tests|
|-------------------------|-----|
|Tensor core              |14   |
|Tokenizer                |9    |
|Attention + FFN          |10   |
|Loss + Gradients         |14   |
|RSSM (fixed + learned)   |12   |
|Distributed scan         |12   |
|Validator + backpressure |14   |
|Receipt + audit chain    |20   |
|Training run + manifest  |18   |
|Phase contracts (6, 7, 8)|29   |
|OWT loader + training    |8    |
|Integration + other      |308  |

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
  finite_difference_gradient.fard
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
  test_*.fard  (88 files)

out/checkpoints/
  shard_0.json .. shard_79.json
```

-----

## Running

```
fardrun test --program tests/test_train_step.fard
fardrun test --program tests/test_rssm_learned.fard
fardrun test --program tests/test_owt_loader.fard
fardrun test --program tests/test_owt_train.fard
fardrun run  --program main.fard --out out/main_run
fardrun run  --program main_owt.fard --out out/owt_full_run
```

-----

## License

MUI