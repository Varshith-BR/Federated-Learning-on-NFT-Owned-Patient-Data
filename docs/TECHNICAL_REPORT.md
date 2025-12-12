# Federated Learning on NFT-Owned Patient Data
## Technical Report for Summit Presentation

**Project:** Privacy-Preserving Healthcare ML with Blockchain Consent Management  
**Date:** December 2025  

---

## Executive Summary

This project implements a **privacy-preserving federated learning system** for healthcare data, integrated with **NFT-based patient consent management** on a blockchain. The system achieves **95.60% validation accuracy** using ensemble machine learning while ensuring that patient data never leaves the hospital servers.

### Key Achievements
- ✅ **95.60% Accuracy** with Random Forest ensemble model
- ✅ **8 Hospital Nodes** participating in federated training
- ✅ **6,569 Consented Patients** contributing data
- ✅ **Real-time Consent Management** via NFT tokens
- ✅ **Zero Data Leakage** - raw patient data never centralized

---

## 1. Problem Statement

### The Healthcare Data Dilemma
- **Challenge**: AI/ML models for healthcare require large, diverse datasets
- **Barrier**: Privacy regulations (HIPAA, GDPR) prevent data centralization
- **Result**: "Data Silos" limiting medical AI development

### Existing Solutions' Limitations
- Traditional FL lacks **patient-level consent control**
- No mechanism for **dynamic consent revocation**
- Missing **audit trail** for data usage

---

## 2. Solution Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                         │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│  │   Patient    │ │   Hospital   │ │    Admin     │            │
│  │   Portal     │ │   Portal     │ │  Dashboard   │            │
│  └──────────────┘ └──────────────┘ └──────────────┘            │
├─────────────────────────────────────────────────────────────────┤
│                    FEDERATED LEARNING LAYER                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │     Central Aggregation Server (FedAvg Algorithm)       │   │
│  │  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐      │   │
│  │  │Node 1│  │Node 2│  │Node 3│  │ ...  │  │Node 8│      │   │
│  │  │ 843  │  │ 800  │  │ 819  │  │      │  │ 801  │      │   │
│  └──────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│                      BLOCKCHAIN LAYER                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  NFT Consent Tokens │ Smart Contracts │ Immutable Ledger │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Machine Learning Models

### Model Performance Summary

| Model | Type | Train Acc | Val Acc | Use Case |
|-------|------|-----------|---------|----------|
| **Random Forest** | Ensemble (Bagging) | 100% | **95.60%** | Primary - Best generalization |
| **Neural Network** | Deep Learning | ~98% | **~92%** | Complex pattern recognition |
| **Gradient Boosting** | Ensemble (Boosting) | ~99% | **~94%** | Robust sequential learning |

### Random Forest Configuration (Primary Model)
- **Estimators**: 100 decision trees
- **Max Depth**: 10 levels
- **Min Samples Split**: 5
- **Parallel Processing**: Enabled

### Neural Network Architecture
- **Input Layer**: 12 features (8 medical + 4 engineered)
- **Hidden Layers**: 128 → 64 → 32 neurons (ReLU activation)
- **Optimizer**: Adam (learning rate = 0.001)
- **Regularization**: L2 (alpha=0.0001)

### Feature Engineering (12 Total Features)

| Original Features (8) | Engineered Features (4) |
|----------------------|-------------------------|
| age | bp_ratio (systolic/diastolic) |
| systolic_bp | metabolic_score (glucose+cholesterol)/2 |
| diastolic_bp | cardiovascular_risk (bp×heart_rate) |
| heart_rate | body_health (BMI×age) |
| temperature | |
| glucose_level | |
| cholesterol | |
| bmi | |

### Classification Task

**Binary Classification: High Risk vs Low Risk Patients**

A patient is **High Risk** if they have ≥2 of these factors:
- Systolic BP > 130 (Hypertension)
- Glucose > 126 (Pre-diabetic)
- Cholesterol > 200 (Borderline high)
- BMI > 28 (Overweight)
- Age > 55 (Age-related risk)

---

## 4. Per-Hospital Training Results

| Hospital | Samples | High Risk | Low Risk | Val Accuracy |
|----------|---------|-----------|----------|--------------|
| Metro General Hospital | 843 | 528 | 315 | **96.45%** |
| Regional Healthcare | 800 | 500 | 300 | **96.25%** |
| St. Mary's Hospital | 819 | 536 | 283 | **90.24%** |
| University Medical | 834 | 512 | 322 | **98.20%** |
| Community Health Network | 833 | 499 | 334 | **92.81%** |
| City Medical Center | 796 | 470 | 326 | **98.12%** |
| Veterans Affairs Hospital | 843 | 537 | 306 | **96.45%** |
| Children's Medical Center | 801 | 497 | 304 | **96.27%** |

**Global Average: 95.60% Validation Accuracy**

---

## 5. Dataset Statistics

| Metric | Value |
|--------|-------|
| Total Patients | 10,000 |
| Consented Patients | 6,856 (68.56%) |
| Active Hospital Nodes | 8 |
| Features Used | 12 |
| High Risk Patients | ~60% |
| Low Risk Patients | ~40% |

---

## 6. Privacy & Consent Metrics

- **Data Centralization**: ❌ None (0 raw records shared)
- **Consent Verification**: ✅ Real-time NFT check
- **Audit Trail**: ✅ Immutable blockchain log
- **Patient Control**: ✅ Grant/revoke anytime

---

## 7. Demo Instructions

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the server
python app.py

# 3. Access dashboard
# Open: http://localhost:5000/training
```

### Training Demo Steps:
1. Navigate to **Training Dashboard**
2. Select **Model Type**: Random Forest, Neural Network, or Gradient Boosting
3. Set **Training Rounds**: 2-3 (recommended)
4. Click **Start Training**
5. Observe real-time metrics

---

## 8. Conclusion

✅ **Privacy-preserving ML** with 95.60% accuracy  
✅ **Blockchain-based consent** with NFT tokens  
✅ **Federated learning** across 8 hospital nodes  
✅ **Dynamic patient control** over data usage  

---

**End of Technical Report**
