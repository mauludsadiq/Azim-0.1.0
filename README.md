# Azim Trial

Azim Trial is a deterministic tiny model package written in FARD. It combines:

1. deterministic longest-match tokenization,
2. pure row-major tensor operations,
3. fixed arithmetic weights,
4. a single-block decoder-style neural pass,
5. explicit semantic/world-state verification,
6. canonical JSON SHA-256 receipts.

The package is not a chatbot. It is a receipt-verifiable claim classifier and proof-object generator.

## Package layout

```text
packages/azim_trial/tokenizer.fard   Deterministic tokenizer and tokenizer receipts
packages/azim_trial/tensor.fard      Pure FARD vector/matrix operations
packages/azim_trial/weights.fard     Fixed deterministic model weights
packages/azim_trial/semantic.fard    Explicit world-state predicate evaluator
packages/azim_trial/model.fard       Tiny neural pass + semantic verdict integration
packages/azim_trial/receipts.fard    Package manifest and receipt chaining
tests/*.fard                         Unit tests
examples/*.fard                      Runnable examples
main.fard                            Default run target
```

## Determinism rules

- No runtime randomness.
- No dropout.
- No async or parallel map.
- No hash-dependent map iteration.
- Records are canonicalized before hashing.
- All receipts use `json.canonicalize` and `hash.sha256_text`.
- Ties in `argmax` choose the lowest index.

## Run

```bash
fardrun run --program main.fard --out out/azim_trial
```

## Test

```bash
fardrun test --program tests/test_tokenizer.fard
fardrun test --program tests/test_tensor.fard
fardrun test --program tests/test_semantic.fard
fardrun test --program tests/test_model.fard
```

Or:

```bash
for f in tests/test_*.fard; do fardrun test --program "$f"; done
```

## Example claims

Accepted:

```fard
{ predicate: "has-color", subject: "sky", property: "color", value: "blue" }
```

Rejected:

```fard
{ predicate: "has-color", subject: "sky", property: "color", value: "green" }
```

Needs evidence:

```fard
{ predicate: "has-color", subject: "moon", property: "color", value: "blue" }
```

## Model boundary

The neural pass is deterministic and traced, but the semantic/world-state evaluator is authoritative for the final verdict in v0.1. This prevents the tiny untrained model from hallucinating truth. The neural pass proves the mechanical transformer path exists; the semantic model proves the claim decision.

## Version

Azim Trial v0.1.0 for FARD v1.7.x.
