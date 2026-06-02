# Azim

Deterministic distributed AI training on FARD.

Azim is a training system built on deterministic execution, cryptographic receipts, replay-verifiable distributed computation, validator-supervised optimization, and lawful output constraints. Pure FARD — no Python, no external ML libraries, 14,683 lines of code.

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

Multi-language code training. FARD + Python + JavaScript. 74 files. Compounding.

```
Round 1: 5.3168 → 5.3127  (3,700 steps)
Round 2: 4.2877 → 4.2842  (7,400 steps)
Round 3: 3.9042 → 3.9009  (11,100 steps)
Round 4: 3.5881 → 3.5849  (14,800 steps)
Round 5: 3.3881 → 3.3849  (18,500 steps)

Random baseline: 4.86 (ln 129)
Current loss:    3.38
Below random:    30%
```

Per-language loss after 14,800 steps:

```
python      : 35 files, avg 2.11, min 1.43  (56.5% below random)
javascript  :  9 files, avg 2.96, min 2.23  (39.2% below random)
fard        : 30 files, avg 5.49             (still above random — long files, dense syntax)
```

Code-only training (Python + JS algorithm repos). 44 files. 35,200 steps.

```
Final loss: 1.44  (70% below random baseline)
```

Benchmark suite: 4/4 passing (determinism, receipt, diversity, integrity).

-----

## Coding Agent

Azim now includes a live coding agent that uses an external LLM to propose code, executes it, and accepts only what runs — with cryptographic receipts on every step.

```
task: "write a python function called add that takes two numbers and returns their sum"
→ gpt-4o-mini proposes: def add(a, b): return a + b / print(add(2, 3))
→ Azim executes: python3 candidate.py
→ stdout: 5
→ accepted on attempt 1
→ receipt: sha256:652c31f7...
```

The full chain — task → LLM proposal → execution → verification → receipt — is deterministic and auditable. Every failed attempt is also receipted, including the stderr that triggered the feedback prompt.

**Feedback loop:** if a candidate fails, the error is fed back to the LLM as context for a revised attempt. The agent retries up to N times, accepting the first candidate that executes successfully.

-----

## Status

|Milestone                                   |Status|
|--------------------------------------------|------|
|Deterministic runtime (FARD)                |done  |
|Cryptographic receipt chain                 |done  |
|Full OWT training runs                      |done  |
|linalg native ops (28x speedup)             |done  |
|Multi-language tokenizer (159 tokens)       |done  |
|BPE tokenizer (500 merges, vocab 600)       |done  |
|Verifier-gated self-training loop           |done  |
|Scale gate with language diversity          |done  |
|Architecture (d_model=32, n_layers=2)       |done  |
|Blockwise multi-direction SPSA all weights  |done  |
|Deterministic samplers                      |done  |
|CLI + benchmark suite (4/4)                 |done  |
|Language control tokens                     |done  |
|Execution verifiers (Python, JS, Rust, FARD)|done  |
|Unit-test harness                           |done  |
|HumanEval runner                            |done  |
|GitHub corpus acquisition                   |done  |
|Task-conditioned generation                 |done  |
|Feedback loop (stderr → revised candidate)  |done  |
|Coding agent (LLM + Azim verifier)          |done  |
|Multi-language code training (active)       |active|
|Scale to d_model=128 (cloud GPU)            |next  |
|HumanEval benchmark scores                  |next  |

-----

## Roadmap to GPT-2 Scale

|Phase|Params|GPU hours|Target                                    |
|-----|------|---------|------------------------------------------|
|A1   |6M    |~50      |Real language patterns, HumanEval baseline|
|A2   |30M   |~200     |HumanEval meaningful scores               |
|A3   |85M   |~500     |GPT-2 small equivalent                    |

Total compute: ~1,050 A100-hours, ~$1,575.

LTFF application submitted. Awaiting response.

-----

## Architecture

```
d_model: 32, n_layers: 2, vocab: 129 (character-level), params: ~50,000
Blockwise multi-direction SPSA — all weights — deterministic — receipted
```

-----

## Corpus

```
44 algorithm files (Python + JS) — verified executable, receipted
30 FARD files (azim_trial packages) — repacked to 129-token vocab
Total: 74 files, character-level tokenized, language control tokens prepended
```

-----

## CLI

```
fardrun run --program azim.fard --out <out> -- generate --prompt "..." --mode topk
fardrun run --program run_benchmark.fard --out out/benchmark
```

-----

## Coding Agent Usage

```
# Requires .openai_key file (never committed)
fardrun run --program test_agent_live.fard --out out/agent_result

# Or call directly:
agent.run_agent(task, lang, max_attempts, candidate_dir, run_dir, api_url, key, model)

# Compatible with any OpenAI-compatible API:
# - OpenAI: https://api.openai.com/v1/chat/completions
# - Gemini: https://generativelanguage.googleapis.com/v1beta/openai/chat/completions
```

-----

## Test Coverage

191 test files. 0 failures.

-----

## Repository Structure

```
packages/azim_trial/         — core LM training system
packages/azim_code/
  verifier.fard              — execution verifiers (Python, JS, Rust, FARD)
  test_harness.fard          — unit-test runner
  humaneval_runner.fard      — HumanEval pass/fail with receipts
  corpus_acquire.fard        — GitHub corpus acquisition
  code_train_adapter.fard    — train on verified code corpus
  task_generator.fard        — task-conditioned generation + feedback loop
  coding_agent.fard          — LLM coding agent with execution verification
  tokenizer.fard             — 159-token multi-language tokenizer
  scale_gate.fard            — evidence + diversity gated scaling
  loop_run.fard              — full self-training loop

azim.fard                    — CLI
run_benchmark.fard           — benchmark suite
train_full_corpus.fard       — full corpus training (FARD+Python+JS)
test_agent_live.fard         — live coding agent test

.gitignore                   — .openai_key and test files with secrets excluded
```

-----

## License

MUI