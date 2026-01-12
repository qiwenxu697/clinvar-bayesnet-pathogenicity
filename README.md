# ClinVar Bayesian Network for Variant Pathogenicity Prediction

An interpretable **Bayesian Network (BN)** model for predicting whether a human genetic variant is **benign or pathogenic**, built using curated data from **ClinVar**. This project demonstrates how probabilistic graphical models can capture biologically meaningful dependencies while handling uncertainty and class imbalance in large-scale genomic data.

---

## Overview

Whole-genome sequencing identifies millions of genetic variants per individual, but only a small fraction are clinically relevant. Experimentally validating each variant is infeasible, making **computational prioritization essential**.

In this project, we construct a **discrete Bayesian Network** that predicts variant pathogenicity using engineered genomic and clinical features derived from ClinVar. Unlike black-box models, the BN provides **interpretable structure and conditional probability tables (CPTs)** that reveal how different biological factors interact.

**Key idea:** Even with a limited, high-level feature set, probabilistic modeling can recover meaningful biological signal and provide calibrated uncertainty estimates.

---

## Dataset

- **Source:** ClinVar `variant_summary.txt.gz` (NCBI)
- **Scope:** Millions of curated human genetic variants (GRCh37 / GRCh38)
- **Target label:** `ClinSigSimple`
  - `0` → benign-like
  - `1` → pathogenic-like

Variants missing critical fields (e.g., chromosome, position, gene symbol) were removed to ensure well-defined feature construction.

---

## Feature Engineering

We engineered discrete, biologically motivated features that reflect known mechanisms of pathogenicity:

| Feature | Description |
|------|------------|
| **VariantType** | SNV, deletion, indel, CNV, other |
| **Frameshift** | Whether insertion/deletion length is not divisible by 3 |
| **StopGain** | Approximate detection of premature stop codons via HGVS parsing |
| **LengthChange_bin** | SNV (1 bp), small indel (2–20 bp), large indel (>20 bp) |
| **Chromosome_clean** | autosome, sex chromosome, mitochondrial, unknown |
| **PositionBin** | Genomic location binned into low / mid / high regions |
| **GeneGroup** | Functional grouping (tumor suppressor, metabolism, DNA repair, etc.) |

### Leakage Control

Several downstream features (frameshift, stop-gain, length change, positional bins) were found to introduce **deterministic leakage** into the target label. These features were **removed from the final model**, ensuring predictions rely only on upstream, biologically plausible information.

---

## Model

### Bayesian Network

- **Structure learning:** Hill Climb Search with **BIC scoring**
- **Constraints:**
  - Target node (`ClinSigSimple`) only has **incoming edges**
  - Maximum of **4 parents per node**
- **Parameter learning:** Maximum Likelihood Estimation (MLE)
- **Inference:** Exact inference via **Variable Elimination**

This approach balances interpretability, scalability, and robustness under extreme class imbalance.

---

## Learned Network Structure

The final DAG contains six edges, including:

- `VariantType → ClinSigSimple`
- `GeneGroup → ClinSigSimple`
- `Chromosome_clean → ClinSigSimple`
- Dependencies among `VariantType`, `GeneGroup`, and `Chromosome_clean`

These relationships reflect known biological patterns, such as mutation type and gene function being strong predictors of pathogenicity.

---

## Results

**Evaluation split:** 80% train / 20% test (≈ 7.9M test variants)

| Metric | Value |
|------|------|
| Accuracy | **0.917** |
| ROC-AUC | **0.737** |
| PR-AUC | **0.376** |
| Precision (pathogenic) | **0.624** |
| Recall (pathogenic) | **0.303** |
| F1 (pathogenic) | **0.408** |

> Pathogenic variants make up only **9.4%** of the dataset.  
> A PR-AUC of **0.376** is ~4× higher than the random baseline, demonstrating meaningful signal capture despite severe imbalance.

---

## Interpretability & Insights

- Certain variant types (e.g., indels) carry higher pathogenic risk
- Gene functional categories significantly influence predictions
- Chromosomal context provides non-trivial predictive information
- CPT inspection reveals biologically reasonable distributions rather than opaque decision boundaries

---

## Limitations

- Binary pathogenicity label oversimplifies clinical reality
- Lack of conservation scores (PhyloP, GERP) and protein structural annotations
- Discretization may lose fine-grained information
- Recall remains limited for pathogenic variants

---

## Future Work

- Incorporate evolutionary conservation and protein-level features
- Extend to multi-class or graded pathogenicity prediction
- Hybrid Bayesian models with continuous variables
- Integration with downstream clinical decision-support systems

---

## Authors

* Qiwen Xu
* Michael Kroyan
* Janice Rincon
* Vibusha Vadivel
* Jiya Makhija


## Repository Structure

