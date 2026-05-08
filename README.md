# Azim v0.1.0

Azim is a deterministic AI architecture implemented in FARD.

The system separates:

- recurrent world-state memory
- linguistic realization
- deterministic optimization
- lawful generation
- hardware-independent verification

into independently verifiable subsystems.

Every subsystem emits deterministic SHA-256 receipts.

Azim is not a stochastic monolithic transformer.

It is a structurally separated architecture designed around:

- deterministic execution
- replay verification
- causal isolation
- lawful realization
- reproducible optimization
- hardware-independent validation

---

# System Overview

Azim consists of two primary computational systems:

| System | Responsibility |
|---|---|
| RSSM | world-state memory |
| Aware-Tower | linguistic competence |

These systems communicate through a constrained deterministic bridge.

---

# Deterministic Invariant

Core invariant:

text id="7smbd8" same inputs -> same outputs -> same receipts 

Receipts commit to:

- inputs
- outputs
- execution structure
- runtime configuration
- subsystem state
- implementation details

---

# Phase 0 — Deterministic Runtime

Implemented:

- tokenizer
- tensor algebra
- embedding
- attention
- transformer blocks
- logits
- generation
- semantic validation
- replay receipts

Subsystems:

text id="s44f09" tokenizer tensor embedding attention block logits generation semantic validator 

---

# Phase 1 — Aware-Tower

The Aware-Tower separates language into hierarchical causal layers.

Hierarchy:

text id="zlt0li" L0 phoneme L1 morpheme L2 lemma L3 word L4 phrase L5 clause L6 discourse 

Implemented:

- cross-layer attention
- FiLM modulation
- lawful realization algebra
- causal independence verification
- tower receipts

Cross-layer structure:

text id="07k5z5" L1 attends to L0 L2 attends to L1 ... L6 attends to L5 

Independence verified:

text id="ib7h9u" zero L3 -> L0 remains stable 

This confirms higher-level structure does not collapse lower-level representations.

---

# Morphological Realization

Azim does not emit unconstrained arbitrary text.

The tower emits structured realization constraints:

text id="pm65qx" (lemma_id, class_id) 

mapped through a lawful realization algebra:

text id="2bq65e" ("sky", "noun_plural") -> "skies" 

Implemented:

- realization maps
- lawful pair verification
- surface generation
- realization receipts

Illegal realization pairs fail safely.

---

# Phase 2 — RSSM

The RSSM handles recurrent semantic memory and world-state evolution.

Implemented:

- recurrent latent state transitions
- deterministic recurrence
- associative scan
- RSSM ↔ Tower bridge
- structural allocation
- leakage monitoring
- scale manifests

Core recurrence:

text id="xwhu6d" h_t = f(h_(t-1), x_t) 

Associative scan verified:

text id="m1hqgu" parallel scan == sequential recurrence 

This establishes deterministic parallel recurrent execution.

---

# RSSM ↔ Tower Separation

Azim separates:

| Component | Responsibility |
|---|---|
| RSSM | semantic memory |
| Tower | syntax and realization |

Bridge implemented:

text id="x6qqxm" RSSM attends to Tower L6 Tower attends to RSSM hidden state 

Structural allocation enforced:

text id="s0nkk3" RSSM  = 80% Tower = 20% 

---

# Leakage Detection

Leakage probes verify the RSSM does not absorb syntax responsibilities.

Implemented:

- syntax probes
- semantic probes
- cosine monitoring
- leakage thresholds
- deterministic receipts

Leakage condition:

text id="0pqibz" rssm_score >= tower_score 

Clean separation:

text id="d2c7iu" rssm_score < tower_score 

---

# Phase 3 — Gradient Oracle

Azim replaces unconstrained stochastic optimization with deterministic directional search.

Implemented:

- 8-direction orthogonal oracle
- finite-difference gradients
- hybrid oracle
- cosine variance monitoring
- basis expansion triggers
- medium-scale manifests

---

# 8-Direction Orthogonal Oracle

The oracle evaluates deterministic orthogonal update directions.

Implemented:

- orthogonal basis generation
- directional derivatives
- oracle scoring
- deterministic oracle receipts

Oracle search:

text id="0o2ws6" 8 orthogonal update directions 

instead of unconstrained stochastic parameter updates.

---

# Hybrid Oracle

The hybrid oracle combines:

| Component | Role |
|---|---|
| gradient hint | fast directional guidance |
| discrete oracle | deterministic constrained search |

This preserves deterministic guarantees while improving convergence speed.

Implemented:

- gradient hints
- direction alignment scoring
- best-direction selection
- hybrid receipts

---

# Gradient Variance Monitoring

Variance monitoring tracks cosine similarity between consecutive updates.

Implemented:

- vector norms
- cosine similarity
- basis expansion triggers
- deterministic variance receipts

Examples:

text id="r6mjxj" same direction      -> 1.0 orthogonal updates  -> 0.0 

Basis expansion trigger:

text id="wqv5pb" cos_sim < 0.5 

---

# Medium-Scale Training

Implemented manifests for:

| Scale | Parameters |
|---|---|
| medium | 100M |
| medium | 250M |
| medium | 500M |

Each verifies:

- hybrid oracle usage
- variance monitoring
- structural allocation
- deterministic receipts

---

# Phase 4 — Dual-Receipt Protocol

Phase 4 introduces hardware-independent verification.

Azim separates:

| Receipt | Meaning |
|---|---|
| math_receipt | mathematical truth |
| impl_receipt | hardware/runtime realization |

This allows identical mathematical execution to verify across different hardware implementations.

---

# Dual-Receipt Schema

Implemented:

- math receipts
- implementation receipts
- dual verification reports
- deterministic forensic receipts

Core invariant:

text id="j1i5j0" same math != same implementation 

Different runtimes may produce different implementation traces while preserving identical mathematical truth.

---

# Deterministic Tiling Engine

Implemented:

- configurable tiling
- blocked matvec execution
- tile-aware implementation receipts
- math-stable execution receipts

Verified:

text id="k1kqf7" same math receipt across tile sizes 

while implementation receipts differ.

---

# Cross-Hardware Verification

Implemented:

- CPU/GPU verification
- cross-hardware receipt comparison
- implementation divergence verification
- mathematical equivalence validation

Verified:

text id="yt1m59" cpu.math_receipt == gpu.math_receipt 

while:

text id="2y4x53" cpu.impl_receipt != gpu.impl_receipt 

This establishes hardware-independent mathematical verification.

---

# Large-Scale Training

Implemented manifests for:

| Scale | Parameters |
|---|---|
| large | 500M |
| large | 750M |
| large | 1B |

Each verifies:

- dual-receipt enforcement
- cross-hardware verification
- structural allocation
- deterministic receipts

---

# Current Status

text id="53mlik" Phase 0 ✓ Deterministic Runtime Phase 1 ✓ Aware-Tower Phase 2 ✓ RSSM + Associative Scan Phase 3 ✓ Gradient Oracle Phase 4 ✓ Dual-Receipt Protocol 

Implemented verification domains:

- deterministic execution
- lawful realization
- recurrent memory
- associative recurrence
- structural isolation
- leakage monitoring
- orthogonal optimization
- cosine variance analysis
- medium-scale manifests
- dual-receipt verification
- deterministic tiling
- cross-hardware validation
- large-scale manifests

---

# Repository Structure

text id="u4ljtq" packages/azim_trial/ tests/ 

Major modules:

text id="4s8xj8" tokenizer tensor embedding attention block cross_tower film realization surface rssm rssm_tower_bridge associative_scan structural_allocation leakage_probe scale_manifest gradient_oracle hybrid_oracle gradient_variance medium_training_manifest dual_receipt tiling_engine cross_hardware_verify large_training_manifest 

---

# Running Tests

Gradient oracle:

bash id="h0q0qc" fardrun test --program tests/test_gradient_oracle.fard 

Variance monitoring:

bash id="9udcde" fardrun test --program tests/test_gradient_variance.fard 

Cross-hardware verification:

bash id="u06xdk" fardrun test --program tests/test_cross_hardware_verify.fard 

Large manifests:

bash id="w5phdu" fardrun test --program tests/test_large_training_manifest.fard 

---

# Design Objective

Azim is testing whether AI systems can be built around:

- deterministic execution
- replay verification
- lawful realization
- recurrent world models
- orthogonal optimization
- hardware-independent verification
- structurally separated cognition

instead of opaque stochastic monolithic transformers.

The architecture attempts to preserve:

- deterministic recurrence
- replay-verifiable training
- lawful generation
- scalable recurrent memory
- causal isolation
- deterministic optimization trajectories
- forensic-grade hardware verification