# Azim v0.1.0

Azim is a deterministic experimental architecture implemented in FARD.

It separates:

- linguistic competence
- world-state memory
- realization lawfulness
- replay-verifiable execution

into independently testable subsystems.

Every major subsystem emits deterministic SHA-256 receipts.

The system is designed around four principles:

1. deterministic execution
2. causal architectural separation
3. replay-verifiable training/inference
4. lawful realization constraints

---

# Architecture

Azim is composed of two primary systems:

| System | Role |
|---|---|
| RSSM | world-state memory and latent recurrence |
| Aware-Tower | linguistic competence and realization |

The systems communicate through a constrained bridge.

---

# Phase 0 — Deterministic Runtime

Implemented:

- tokenizer
- tensor algebra
- embedding
- attention
- transformer block
- logits
- generation
- semantic validation
- receipt generation

Core property:

text same inputs -> same outputs -> same receipts 

---

# Phase 1 — Aware-Tower

Implemented:

- 7-layer hierarchy
- cross-layer attention
- FiLM modulation
- realization algebra
- lawful surface generation
- causal independence probes

Tower hierarchy:

text L0 phoneme L1 morpheme L2 lemma L3 word L4 phrase L5 clause L6 discourse 

Causal independence verified:

text zero L3 -> L0 remains stable 

This confirms top-down modulation does not collapse lower-level structure.

---

# Morphological Realization

Azim does not directly emit arbitrary text.

The tower emits structured realization constraints:

text (lemma_id, class_id) 

which are mapped through a lawful realization algebra:

text ("sky", "noun_plural") -> "skies" 

Illegal pairs fall back safely.

Implemented:

- realization maps
- lawful pair verification
- surface generation
- deterministic realization receipts

---

# Phase 2 — RSSM

Implemented:

- latent recurrent state model
- deterministic recurrence
- associative scan equivalence
- RSSM ↔ Tower bridge
- structural allocation
- leakage probes
- scale manifests

RSSM recurrence:

text h_t = f(h_(t-1), x_t) 

Associative scan verified:

text parallel scan == sequential recurrence 

This establishes deterministic parallelizable recurrence.

---

# RSSM ↔ Tower Separation

Azim explicitly separates:

| Component | Responsibility |
|---|---|
| RSSM | world-state memory |
| Tower | linguistic realization |

Bridge implemented:

text RSSM attends to Tower L6 Tower attends to RSSM hidden state 

Structural allocation enforced:

text RSSM  = 80% Tower = 20% 

---

# Leakage Detection

Leakage probes verify the RSSM is not learning syntax.

Implemented:

- syntax probe
- semantic probe
- leakage thresholds
- deterministic probe receipts

Leakage condition:

text rssm_score >= tower_score 

Clean split condition:

text rssm_score < tower_score 

---

# Scale Manifest

Implemented deterministic manifests for:

| Scale | Parameters |
|---|---|
| small | 10M |
| medium | 50M |
| large | 100M |

Each scale preserves:

- RSSM/Tower allocation
- receipt determinism
- bridge structure
- replayability

---

# Deterministic Receipts

All major subsystems emit SHA-256 receipts.

Examples:

- tokenizer receipt
- embedding receipt
- attention receipt
- realization receipt
- RSSM receipt
- bridge receipt
- scan receipt
- leakage receipt
- scale manifest receipt

Receipts commit to:

- inputs
- outputs
- configuration
- execution structure

---

# Current Status

text Phase 0 ✓  Deterministic Runtime Phase 1 ✓  Aware-Tower Phase 2 ✓  RSSM + Bridge + Scan + Allocation + Leakage 

Implemented test domains:

- runtime determinism
- transformer execution
- realization lawfulness
- recurrent state evolution
- bridge grounding
- causal independence
- parallel scan equivalence
- structural allocation
- leakage detection

---

# Repository Structure

text packages/azim_trial/ tests/ 

Subsystems include:

text tokenizer tensor embedding attention block tower cross_tower film realization surface rssm rssm_tower_bridge associative_scan structural_allocation leakage_probe scale_manifest 

---

# Running Tests

Run individual tests:

bash fardrun test --program tests/test_rssm.fard 

Run bridge tests:

bash fardrun test --program tests/test_rssm_tower_bridge.fard 

Run scan tests:

bash fardrun test --program tests/test_associative_scan.fard 

Run leakage tests:

bash fardrun test --program tests/test_leakage_probe.fard 

---

# Design Goal

Azim is not attempting to build a conventional monolithic transformer.

The architecture explicitly separates:

- recurrence
- syntax
- realization
- semantic memory
- lawful generation

into deterministic replay-verifiable components.

The objective is to test whether architectural separation can preserve:

- causal independence
- deterministic recurrence
- lawful realization
- replay verification
- scalable recurrent memory

inside a fully deterministic execution environment.