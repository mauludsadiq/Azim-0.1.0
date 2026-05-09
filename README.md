# Azim

Deterministic distributed AI training on FARD.

Azim is an auditable training architecture built on deterministic execution, cryptographic receipts, replay-verifiable distributed computation, validator-supervised optimization, and lawful output constraints. Pure FARD — no Python, no external ML libraries, 7,941 lines of code.

-----

## What Azim Does

Azim trains a neural model deterministically from tokenization through gradient descent, with every step cryptographically receipted and replay-verifiable.

The training pipeline:

- Tokenizes input text with a fixed greedy vocabulary
- Embeds tokens into distinct 8-dimensional vectors per token ID
- Runs a transformer block: RMS norm, attention, FFN, residual
- Computes NLL loss over three-class label logits
- Computes finite-difference gradients over W_U against the real loss
- Updates W_U via SGD with verified loss decrease per step
- Trains RSSM transition matrices with convergence verification
- Distributes training across nodes with prefix-chained associative scan
- Supervises with real leakage detection and tower independence probes
- Chains SHA-256 receipts over every computed output

-----

## Architecture

|Phase|Description                                                               |
|-----|--------------------------------------------------------------------------|
|0    |Deterministic Runtime (FARD)                                              |
|1    |Aware-Tower — semantic realization with lawful output constraints         |
|2    |RSSM + Associative Scan — learned state evolution, distributed prefix scan|
|3    |Gradient Oracle — finite-difference gradients over real NLL loss          |
|4    |Dual-Receipt Protocol — math and impl receipts independently auditable    |
|5    |Dynamic Basis Expansion — cosine similarity monitoring, expansion events  |
|6    |Distributed Training — three-node cluster with real RSSM train steps      |
|7    |Async Validator — leakage probe, tower independence, backpressure control |
|8    |Full Run + Audit Proof — end-to-end receipt chain with final proof        |

-----

## Training

W_U (3x8) is trained via finite-difference gradient descent.

For each example (text, label):

```
hidden = rms_norm(block(embed(tokenize(text))))
logits = W_U . hidden
loss   = NLL(logits, label)
grad   = finite_difference(loss, W_U, e=0.001)
W_U    = W_U - lr * grad
```

Loss decreases per step. Verified by test.

The RSSM trains W_h against a target state:

```
s_{t+1} = relu(W_h . s_t + W_x . x_t)
loss    = ||s_T - target||^2
grad    = finite_difference(loss, W_h, e=0.001)
W_h     = W_h - lr * grad
```

Convergence verified over multiple steps by test.

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

457 tests. 0 failures.

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
|Integration + other      |305  |

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
  openwebtext_full_run.fard
  final_audit_proof.fard

tests/
  test_*.fard
```

-----

## Running

```
fardrun test --program tests/test_train_step.fard
fardrun test --program tests/test_rssm_learned.fard
fardrun test --program tests/test_cluster_run_1p5b.fard
fardrun run  --program main.fard --out out/main_run
```

-----

## License

MUI