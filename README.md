# Azim v0.1.0

Azim is a deterministic AI architecture implemented in FARD.

The architecture separates:

- world-state memory
- linguistic realization
- deterministic optimization
- hardware realization
- distributed verification

into independently verifiable systems with replayable SHA-256 receipts.

Azim is not a monolithic stochastic transformer.

It is a receipt-driven architecture built around:

- deterministic execution
- lawful realization
- recurrent semantic memory
- orthogonal optimization
- hardware-independent verification
- distributed replay
- causal isolation

---

# Core Invariant

text same inputs -> same outputs -> same receipts 

Receipts commit to:

- inputs
- outputs
- execution graph
- runtime configuration
- subsystem state
- optimization path
- implementation strategy

---

# Architecture

| Component | Responsibility |
|---|---|
| RSSM | recurrent semantic memory |
| Aware-Tower | language realization |
| Gradient Oracle | deterministic optimization |
| Dual-Receipt Layer | hardware-independent verification |
| Basis Expansion | adaptive optimization geometry |

---

# Phase 0 — Deterministic Runtime ✓

Implemented:

- tensor algebra
- embedding
- attention
- transformer blocks
- logits
- generation
- semantic validation
- deterministic replay

Core modules:

text tokenizer tensor embedding attention block logits generation semantic validator 

---

# Phase 1 — Aware-Tower ✓

The Aware-Tower separates language into causal hierarchical layers.

Hierarchy:

text L0 phoneme L1 morpheme L2 lemma L3 word L4 phrase L5 clause L6 discourse 

Implemented:

- cross-layer attention
- FiLM modulation
- realization algebra
- causal independence validation
- lawful generation

Verified:

text higher layers do not collapse lower representations 

---

# Morphological Realization

Azim generates language through lawful realization pairs:

text (lemma_id, class_id) 

Example:

text ("sky", "noun_plural") -> "skies" 

Implemented:

- realization maps
- lawful pair validation
- surface realization
- realization receipts

Illegal realization pairs fail safely.

---

# Phase 2 — RSSM + Associative Scan ✓

The RSSM manages recurrent semantic memory.

Implemented:

- recurrent latent transitions
- RSSM ↔ Tower bridge
- associative scan
- structural allocation
- leakage monitoring
- scale manifests

Core recurrence:

text h_t = f(h_(t-1), x_t) 

Associative scan verified:

text parallel scan == sequential recurrence 

This establishes deterministic recurrent parallelization.

---

# RSSM ↔ Tower Separation

Structural allocation enforced:

| Component | Allocation |
|---|---|
| RSSM | 80% |
| Tower | 20% |

RSSM handles semantic memory.

Tower handles syntax and realization.

Leakage probes verify RSSM does not absorb linguistic structure.

Leakage condition:

text rssm_score >= tower_score 

Clean split:

text rssm_score < tower_score 

---

# Phase 3 — Gradient Oracle ✓

Azim replaces unconstrained SGD with deterministic directional optimization.

Implemented:

- 8-direction orthogonal oracle
- finite-difference gradients
- hybrid oracle
- cosine variance monitoring
- basis expansion triggers
- medium-scale manifests

---

# 8-Direction Orthogonal Oracle

Optimization proceeds through deterministic orthogonal directions.

Implemented:

- orthogonal basis generation
- directional derivatives
- oracle scoring
- deterministic receipts

Search space:

text 8 orthogonal update directions 

instead of unconstrained stochastic updates.

---

# Hybrid Oracle

The hybrid oracle combines:

| Component | Role |
|---|---|
| gradient hint | fast directional guidance |
| discrete oracle | deterministic constrained optimization |

This preserves deterministic guarantees while improving convergence.

Implemented:

- gradient hints
- alignment scoring
- direction selection
- hybrid receipts

---

# Gradient Variance Monitoring

Cosine similarity tracks optimization stability.

Implemented:

- vector norms
- cosine similarity
- basis expansion triggers
- variance receipts

Examples:

text same direction     -> 1.0 orthogonal update  -> 0.0 

Expansion trigger:

text cos_sim < 0.5 

---

# Medium-Scale Training

Verified manifests:

| Scale | Parameters |
|---|---|
| medium | 100M |
| medium | 250M |
| medium | 500M |

Each validates:

- hybrid oracle usage
- variance monitoring
- structural allocation
- deterministic receipts

---

# Phase 4 — Dual-Receipt Protocol ✓

Phase 4 introduces hardware-independent verification.

Azim separates:

| Receipt | Meaning |
|---|---|
| math_receipt | mathematical truth |
| impl_receipt | hardware/runtime realization |

Different hardware implementations may differ internally while preserving identical mathematical execution.

---

# Dual-Receipt Invariant

Core invariant:

text same math != same implementation 

Implemented:

- math receipts
- implementation receipts
- dual verification reports
- deterministic forensic receipts

---

# Deterministic Tiling Engine

Implemented:

- configurable tiling
- blocked matvec execution
- tile-aware implementation receipts
- math-stable receipts

Verified:

text same math receipt across tile sizes 

while implementation receipts differ.

---

# Cross-Hardware Verification

Implemented:

- CPU/GPU verification
- cross-hardware receipt comparison
- implementation divergence verification
- mathematical equivalence validation

Verified:

text cpu.math_receipt == gpu.math_receipt 

while:

text cpu.impl_receipt != gpu.impl_receipt 

This establishes hardware-independent mathematical verification.

---

# Large-Scale Training

Verified manifests:

| Scale | Parameters |
|---|---|
| large | 500M |
| large | 750M |
| large | 1B |

Each validates:

- dual-receipt enforcement
- cross-hardware verification
- structural allocation
- deterministic receipts

---

# Phase 5 — Dynamic Basis Expansion ✓

Phase 5 introduces adaptive optimization geometry.

Implemented:

- dynamic basis expansion
- CosSim-triggered expansion
- graph-signed expansion events
- expansion stability validation

Expansion chain:

text 8 -> 16 -> 32 

Expansion triggers when cosine similarity drops below threshold.

---

# Dynamic Expansion

Expansion behavior verified:

text cos_sim < threshold -> expand basis cos_sim >= threshold -> retain basis 

Implemented:

- expansion triggers
- deterministic expansion receipts
- expansion path replay
- basis growth validation

Verified:

text 8 -> 16 16 -> 32 32 -> 32 

---

# Basis Expansion Graph Events

Expansion events are signed into the module graph.

Each event records:

- trigger reason
- cosine similarity
- prior basis size
- next basis size
- event receipt
- graph digest

Replay reproduces the exact optimization expansion path.

---

# Expansion Stability Validation

Implemented:

- max loss delta tracking
- spike detection
- stability thresholds
- deterministic stability receipts

Validated:

text basis expansion does not create loss spikes 

Stability condition:

text max_loss_delta <= threshold 

---

# Current Status

text Phase 0 ✓ Deterministic Runtime Phase 1 ✓ Aware-Tower Phase 2 ✓ RSSM + Associative Scan Phase 3 ✓ Gradient Oracle Phase 4 ✓ Dual-Receipt Protocol Phase 5 ✓ Dynamic Basis Expansion Phase 6 ⬜ Distributed / State Pack CDN Phase 7 ⬜ Asynchronous Validator Phase 8 ⬜ OpenWebText Run 

---

# Repository Structure

text packages/azim_trial/ tests/ 

Major modules:

text tokenizer tensor embedding attention block cross_tower film realization surface rssm rssm_tower_bridge associative_scan structural_allocation leakage_probe scale_manifest gradient_oracle hybrid_oracle gradient_variance medium_training_manifest dual_receipt tiling_engine cross_hardware_verify large_training_manifest basis_expansion basis_graph_events expansion_stability 

---

# Running Tests

Basis expansion:

bash fardrun test --program tests/test_basis_expansion.fard 

Graph event signing:

bash fardrun test --program tests/test_basis_graph_events.fard 

Expansion stability:

bash fardrun test --program tests/test_expansion_stability.fard 

Cross-hardware verification:

bash fardrun test --program tests/test_cross_hardware_verify.fard 

Large manifests:

bash fardrun test --program tests/test_large_training_manifest.fard 

---

# Design Objective

Azim explores whether AI systems can be built around:

- deterministic execution
- replay verification
- recurrent semantic memory
- lawful realization
- orthogonal optimization
- adaptive optimization geometry
- hardware-independent verification
- distributed validation

instead of opaque stochastic monolithic transformers.

The architecture attempts to preserve:

- deterministic recurrence
- replayable optimization
- lawful generation
- causal isolation
- recurrent world models
- forensic hardware verification
- exact optimization replay
- signed adaptive training paths