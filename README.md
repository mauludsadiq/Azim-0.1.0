# Azim v0.1.0

Azim is a deterministic AI architecture implemented in FARD.

The system separates:

- world-state memory
- linguistic realization
- recurrent state evolution
- lawful surface generation
- deterministic optimization

into independently verifiable subsystems.

Every subsystem emits deterministic SHA-256 receipts.

Azim is not a monolithic transformer.

It is a structurally separated architecture built around deterministic execution, replay verification, and causal isolation.

---

# Core Design

Azim consists of two primary computational systems:

| System | Responsibility |
|---|---|
| RSSM | world-state memory |
| Aware-Tower | linguistic competence |

The systems communicate through a constrained deterministic bridge.

---

# Deterministic Execution

All major computations produce replay-verifiable receipts.

Core invariant:

text id="c1jk7w" same inputs -> same outputs -> same receipts 

Receipts commit to:

- inputs
- outputs
- configuration
- execution structure
- subsystem state

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

text id="yxqz4v" tokenizer tensor embedding attention block logits generation semantic validator 

---

# Phase 1 — Aware-Tower

The Aware-Tower separates linguistic structure into hierarchical layers.

Hierarchy:

text id="8ht5ql" L0 phoneme L1 morpheme L2 lemma L3 word L4 phrase L5 clause L6 discourse 

Implemented:

- cross-layer attention
- FiLM modulation
- lawful realization
- causal independence verification
- tower receipts

Cross-layer structure:

text id="7a4bg7" L1 attends to L0 L2 attends to L1 ... L6 attends to L5 

Causal independence verified:

text id="l1qg7i" zero L3 -> L0 remains stable 

This confirms higher layers do not collapse lower-level structure.

---

# Morphological Realization

Azim does not emit arbitrary unconstrained text.

The tower emits structured realization constraints:

text id="4x44c7" (lemma_id, class_id) 

which are mapped through a realization algebra:

text id="bo9vcq" ("sky", "noun_plural") -> "skies" 

Implemented:

- realization maps
- lawful pair verification
- surface generation
- deterministic realization receipts

Illegal realization pairs fall back safely.

---

# Phase 2 — RSSM

The RSSM handles world-state recurrence and latent memory evolution.

Implemented:

- recurrent state transitions
- deterministic recurrence
- associative scan
- RSSM ↔ Tower bridge
- structural allocation
- leakage monitoring
- scale manifests

Core recurrence:

text id="5szr9j" h_t = f(h_(t-1), x_t) 

Associative scan verified:

text id="8m2u1n" parallel scan == sequential recurrence 

This establishes deterministic parallel recurrence.

---

# RSSM ↔ Tower Separation

Azim explicitly separates semantic memory from linguistic realization.

| Component | Responsibility |
|---|---|
| RSSM | semantic/world-state memory |
| Tower | syntax and realization |

Bridge implemented:

text id="bsg7yy" RSSM attends to Tower L6 Tower attends to RSSM hidden state 

Structural allocation enforced:

text id="mznxoe" RSSM  = 80% Tower = 20% 

---

# Leakage Detection

Leakage probes verify that the RSSM does not absorb syntax responsibilities.

Implemented:

- syntax probes
- semantic probes
- cosine monitoring
- leakage thresholds
- deterministic probe receipts

Leakage trigger:

text id="1fch5s" rssm_score >= tower_score 

Clean separation:

text id="e8x4r5" rssm_score < tower_score 

---

# Phase 3 — Gradient Oracle

Azim replaces unconstrained backpropagation with deterministic directional search.

Implemented:

- 8-direction orthogonal oracle
- finite-difference gradients
- hybrid oracle
- cosine variance monitoring
- basis expansion triggers
- medium-scale manifests

---

# 8-Direction Orthogonal Oracle

The oracle evaluates deterministic directional updates across orthogonal basis vectors.

Implemented:

- orthogonal basis generation
- directional derivatives
- oracle scoring
- deterministic oracle receipts

The oracle evaluates:

text id="m0z1jz" 8 orthogonal update directions 

instead of unconstrained stochastic parameter updates.

---

# Hybrid Oracle

The hybrid oracle combines:

| Component | Role |
|---|---|
| gradient hint | fast directional guidance |
| discrete oracle | deterministic constrained search |

This preserves deterministic search guarantees while improving convergence speed.

Implemented:

- gradient hints
- direction alignment scoring
- best-direction selection
- deterministic hybrid receipts

---

# Gradient Variance Monitoring

Variance monitoring tracks cosine similarity between consecutive updates.

Implemented:

- vector norms
- cosine similarity
- basis expansion triggers
- deterministic variance receipts

Examples:

text id="4l5c2r" same direction      -> 1.0 orthogonal updates  -> 0.0 

Basis expansion condition:

text id="7r5n8h" cos_sim < 0.5 

---

# Medium Training Manifest

Medium-scale deterministic manifests implemented for:

| Scale | Parameters |
|---|---|
| medium | 100M |
| medium | 250M |
| medium | 500M |

Each manifest verifies:

- structural allocation
- hybrid oracle usage
- variance monitoring
- replay determinism

---

# Current Status

text id="f5v7qe" Phase 0 ✓ Deterministic Runtime Phase 1 ✓ Aware-Tower Phase 2 ✓ RSSM + Associative Scan Phase 3 ✓ Gradient Oracle 

Implemented verification domains:

- deterministic execution
- transformer hierarchy
- lawful realization
- recurrent state evolution
- associative recurrence
- structural separation
- leakage detection
- orthogonal oracle search
- cosine variance monitoring
- medium-scale manifests

---

# Repository Structure

text id="2n7qht" packages/azim_trial/ tests/ 

Major modules:

text id="s7z7ie" tokenizer tensor embedding attention block cross_tower film realization surface rssm rssm_tower_bridge associative_scan structural_allocation leakage_probe scale_manifest gradient_oracle hybrid_oracle gradient_variance medium_training_manifest 

---

# Running Tests

Example:

bash id="ov4g1m" fardrun test --program tests/test_gradient_oracle.fard 

Variance monitoring:

bash id="3zj4lj" fardrun test --program tests/test_gradient_variance.fard 

Hybrid oracle:

bash id="j4ujm0" fardrun test --program tests/test_hybrid_oracle.fard 

RSSM bridge:

bash id="0dbnbi" fardrun test --program tests/test_rssm_tower_bridge.fard 

---

# Design Objective

Azim is testing whether AI systems can be built around:

- deterministic execution
- replay verification
- constrained realization
- structural separation
- recurrent world models
- orthogonal optimization
- causal independence

instead of monolithic stochastic transformers.

The architecture attempts to preserve:

- deterministic recurrence
- lawful generation
- replay-verifiable training
- scalable recurrent memory
- structurally isolated linguistic competence
- deterministic optimization trajectories