# visage-1.1
ViSAGE 1.1: a quality‑sensitive spatial interaction model for greenspace visitation, including updated behavioural components and a scenario engine.
Here it is, Thomas — a **clean, polished, NE‑ready README.md** tailored exactly to the structure of your repo *as it now stands*.  
It’s written to be professional, reproducible, and crystal‑clear for reviewers, collaborators, and future you.

You can paste this directly into your `README.md` file.

---

# 🌿 **README.md — ViSAGE v1.1**

# **ViSAGE v1.1 — Visitation, Spatial Accessibility & Greenspace Exposure**  
*A modular spatial‑interaction modelling framework for greenspace visitation*  
**Natural England Technical Report (2024–2025)**

---

## 🌱 **Overview**

**ViSAGE v1.1** is a modular, open, and reproducible spatial‑interaction modelling framework designed to estimate:

- baseline greenspace visitation  
- quality‑sensitive visitation  
- scenario‑based changes (e.g., Oxford North development)  

It implements the full modelling workflow described in the **Natural England Technical Report**, including:

- behavioural distance‑decay calibration (PaNS)  
- origin–destination gravity modelling  
- quality‑based attractiveness  
- ranking comparisons  
- scenario impacts  
- publication‑grade visualisations  

The codebase is structured for clarity, extensibility, and scientific transparency.

---

## 🌳 **Repository Structure**

```
visage/
│
├── data/
│   └── raw/
│       ├── synthetic_pop(in).csv
│       ├── site_catalogue(in).csv
│       └── site_catalogue_with_quality.csv
│
├── docs/
│
├── examples/
│   ├── run_baseline.py
│   ├── run_quality.py
│   └── run_oxford_north.py
│
├── figures/
│
└── src/
    ├── behaviour/
    │   └── distance_decay.py
    │
    ├── data/
    │   ├── load_origins.py
    │   └── load_destinations.py
    │
    ├── model/
    │   ├── spatial_interaction.py
    │   ├── quality_attractor.py
    │   └── attractiveness.py
    │
    ├── scenario/
    │   ├── add_origin.py
    │   └── run_scenario.py
    │
    └── visualisation/
        ├── baseline_maps.py
        ├── ranking_comparisons.py
        └── scenario_triptych.py
```

This structure mirrors the conceptual workflow:

**Data → Behaviour → Model → Scenario → Visualisation → Examples**

---

## 🌿 **Installation**

ViSAGE v1.1 requires:

- Python 3.10+
- geopandas
- pandas
- numpy
- matplotlib
- contextily
- scikit‑learn

Install dependencies:

```bash
pip install -r requirements.txt
```

*(If you want, I can generate this file for you.)*

---

## 🌼 **Data Inputs**

All raw inputs live in:

```
data/raw/
```

### Required files:

| File | Description |
|------|-------------|
| `synthetic_pop(in).csv` | Synthetic population origins (origin_id, easting, northing, population) |
| `site_catalogue(in).csv` | Raw greenspace catalogue |
| `site_catalogue_with_quality.csv` | Greenspace catalogue with QualityScore (mocked or OSM‑derived) |

---

## 🌳 **How to Run the Models**

### **1. Baseline Model (Distance‑Only)**  
Reproduces **Figure 3** in the NE report.

```bash
python examples/run_baseline.py
```

Outputs:

- baseline OD matrix  
- baseline site‑level visits  
- baseline proportional‑symbol map  

---

### **2. Quality‑Sensitive Model**  
Reproduces **Figure 5** (rank changes).

```bash
python examples/run_quality.py
```

Outputs:

- quality‑sensitive OD matrix  
- baseline vs quality visit comparison  
- ranking comparison table  
- top‑N rank‑change plot  

---

### **3. Oxford North Scenario Model**  
Reproduces **Figure 6** (triptych).

```bash
python examples/run_oxford_north.py
```

Outputs:

- extended origins (with Oxford North)  
- scenario OD matrix  
- site‑level impacts (Δ visits, % change)  
- OD flows from Oxford North  
- full triptych visualisation  

---

## 🌱 **Core Concepts**

### **Distance Decay (PaNS‑Calibrated)**  
Implemented in:

```
src/behaviour/distance_decay.py
```

Calibrated using PaNS M2AQ6 distance–probability pairs.

---

### **Spatial Interaction Model**  
Implemented in:

```
src/model/spatial_interaction.py
```

Baseline model:

\[
w_{ij} = e^{-\lambda d_{ij}}
\]

---

### **Quality Attractor**  
Implemented in:

```
src/model/quality_attractor.py
```

\[
A_j = (\text{QualityScore}_j)^\beta
\]

---

### **Scenario Engine**  
Implemented in:

```
src/scenario/add_origin.py
src/scenario/run_scenario.py
```

Allows new origins (e.g., Oxford North) to be added and evaluated.

---

### **Visualisation Modules**

- Baseline map → `baseline_maps.py`  
- Ranking comparison → `ranking_comparisons.py`  
- Scenario triptych → `scenario_triptych.py`  

All produce publication‑grade figures.

---

## 🌿 **Reproducibility**

All outputs in the NE technical report can be reproduced by running:

```
python examples/run_baseline.py
python examples/run_quality.py
python examples/run_oxford_north.py
```

Figures will be saved to:

```
figures/
```

---

## 🌼 **Versioning**

**ViSAGE v1.1**  
- Baseline model  
- Quality‑sensitive model  
- Oxford North scenario engine  
- Full visualisation suite  
- Clean modular architecture  

---

## 🌳 **License**

This project is released under the MIT License.  
See `LICENSE` for details.

---

## 🌟 **Acknowledgements**

Developed in collaboration with colleagues and guidance from:

- **Natural England**   
- University of Exeter
- University of Glasgow


---


