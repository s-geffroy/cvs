"""cvs/ Streamlit Home — Phase 1."""
from __future__ import annotations

import streamlit as st

from apps.ui_streamlit.components import ethics_banner

st.set_page_config(page_title="cvs — Civilizational Vector State", layout="wide")
ethics_banner.render()

st.title("Civilizational Vector State (cvs/) — Phase 1 working UI")

st.markdown(
    """
Bienvenue dans l'interface de travail du projet **`cvs/`**.

Le projet repose sur **deux bases** :

- **`B_doc`** (documentaire) — Huntington (1996), Inglehart-Welzel (2005, 2010), Hofstede (2010), WVS wave 7.
- **`B_vec`** (vectorielle) — `B_viz = ℝ²` (Inglehart-Welzel) ⊕ `B_score = ℝ⁶` (Hofstede).

Étendu par :

- **Second moment civilisationnel** `M(s) ∈ ℝ^{6×6}` — dispersion pondérée des centroïdes civilisationnels autour de `xₛ` ; renommé en v3.0 depuis l'ancien « tenseur de tension T(s) » pour évacuer l'analogie mécanique trompeuse (cf. doc 11).
- **Algèbre des distances** : `d_viz`, `d_score^M_intra`, `d_w^W` (Wasserstein-2), `d_M_F`, `d_hyb` — comparaisons rigoureuses entre États.

### Pages

| Page | Rôle |
|---|---|
| **1 — Documentary Basis** | Taxonomie hyper-détaillée, bibliographie, sous-clusters, controverses. |
| **2 — Vector Basis** | Scatter IW 2D, radars Hofstede 6D des 11 centroïdes civilisationnels. |
| **3 — State Explorer** | Profil d'un État : coordonnées, vecteur d'affinité, evidence trace. |
| **4 — Compare States** | Superposition radars/scatter de 2 à 5 États. |
| **5 — Diagnostics** | Couverture des données, citations orphelines, drapeaux qualité. |
| **6 — Sources** | Bibliographie complète + licences. |
| **7 — Methodology** | Docs `00..15` rendus en HTML (incluant critiques, validation, sensibilité, baseline, glossaire). |
| **8 — Second Moment M(s)** | Heatmap M(s) 6×6, valeurs propres, directions principales, décomposition Cov + biais, anisotropie. |
| **9 — Distance Algebra** | Toutes les distances, heatmap, dendrogramme Ward, ajustement `(α, β, γ)`. |

### Commandes utiles

```bash
docker compose build civvec_ui
docker compose up civvec_ui                 # http://localhost:8501
docker compose run --rm civvec_ui civvec basis build
docker compose run --rm civvec_ui pytest
```
"""
)
