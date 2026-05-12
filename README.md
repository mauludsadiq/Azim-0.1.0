# Azim

Deterministic distributed AI training on FARD.

Azim is a training system built on deterministic execution, cryptographic receipts, replay-verifiable distributed computation, validator-supervised optimization, and lawful output constraints. Pure FARD — no Python, no external ML libraries, 10,970 lines of code.

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

LM objective run (next-token prediction). 62/80 shards complete. Loss trend: -0.021 per shard.

-----

## Status

|Milestone                               |Status                |
|----------------------------------------|----------------------|
|Deterministic runtime                   |done                  |
|Cryptographic receipt chain             |done                  |
|Real gradient descent (SPSA)            |done                  |
|Full OWT training run (classifier)      |done                  |
|Neural path authoritative               |done                  |
|Next-token prediction objective         |done                  |
|Autoregressive generation               |done                  |
|linalg native ops (28x speedup)         |done                  |
|Structural tokenizer (language-agnostic)|done                  |
|Verifier-gated self-training loop       |done                  |
|Scale gate                              |done                  |
|LM training on OWT                      |running — 62/80 shards|
|BPE tokenizer                           |next                  |
|Larger d_model / more layers            |next                  |

-----

## What Azim Does

Azim trains a language model on real data with a closed verifier-gated self-improvement loop.

Two training pipelines:

**OWT Pipeline** — trains on real web text:

- Downloads OpenWebText parquet shards from HuggingFace
- Extracts and tokenizes real web text
- Trains W_U_lm via SPSA gradient descent
- Checkpoints with receipt after each shard
- Generates text autoregressively via greedy decoding

**Azim-Code Pipeline** — trains on verified source code:

- Packs source files into tokenized training corpus
- Generates code candidates
- Executes each candidate via fardrun — real execution
- Accepts candidates that run and verify
- Trains on accepted corpus only
- Produces retraining manifest with full cryptographic audit chain
- Gates scale decisions on measured loss decrease + verified receipts

-----

## Structural Tokenizer

Azim includes a language-agnostic structural tokenizer (66 tokens) that understands code at the syntactic level rather than character level.

Token classes:

```
Keywords:   let  fn  if  then  else  import  as  export
            match  while  return  true  false  null  ...
Operators:  !=  ==  <=  >=  &&  ||  ->  =>  |>  ?.  ??  ...
            (  )  {  }  [  ]  ,  :  .  +  -  *  /  =  %  |  <  >
Classes:    <IDENT>  <INT>  <FLOAT>  <STRING>  <BT_STRING>
            <DOC>  <COMMENT>  <NL>  <WS>
```

Features:

- Scans identifiers, numbers (int/float/scientific), strings (quoted/backtick), comments
- Unknown identifiers map to <IDENT> rather than <UNK> — structure is preserved
- Works on any C-like syntax: FARD, Python, JavaScript, Rust, Go
- Every tokenization produces a SHA-256 receipt over input + output + vocab hash
- Used by the Azim-Code self-training pipeline

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

Scale gate result:

```
loss_before: 5.831
loss_after:  5.827
accepted:    3/3
receipts:    3/3
decision:    PASS
```

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
|Code |Verifier-gated self-training on source code                               |

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

141 test files. 0 failures.

|Area                     |Tests|
|-------------------------|-----|
|Tensor core + linalg     |20   |
|Tokenizer (trial)        |9    |
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
|Azim-Code pipeline       |9    |
|Neural authority         |6    |
|Integration + other      |341  |

-----

## Repository Structure

```
packages/azim_trial/       — core LM training system
  tensor.fard              — native linalg ops
  linalg_bridge.fard       — float <-> linalg bytes bridge
  lm_head.fard             — 129-token LM head
  lm_train.fard            — SPSA training with rotating direction
  lm_owt_train.fard        — OWT streaming pipeline
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

tests/
  test_*.fard  (141 files)

out/checkpoints/           — classifier run (80 shards)
out/lm_checkpoints2/       — LM run (62/80 shards, in progress)
```

-----

## Running

```
fardrun test --program tests/test_lm_objective.fard
fardrun test --program tests/test_generation_lm.fard
fardrun run  --program main_lm.fard --out out/lm_full_run
fardrun run  --program test_azim_code_corpus_packer.fard --out out/corpus
fardrun run  --program test_azim_code_train_adapter.fard --out out/code_train
fardrun run  --program test_azim_code_scale_gate.fard --out out/scale_gate
fardrun run  --program main.fard --out out/main_run
```

-----

## License

MUI