# 07 — Politique éthique et publication

> **Avertissement éthique** : Ce profil est inféré à partir de sources publiques agrégées. **Il ne doit pas être utilisé pour classer des individus réels.**

## 1. Avertissement obligatoire sur chaque artefact

Tous les artefacts publiés (pages HTML, JSON, GeoJSON, exports Markdown) **doivent** porter, en clair et de manière visible :

> *Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.*

Implémentation technique :

- Site MkDocs : bannière `announce` non-dismissable via `site_src/overrides/main.html`, vérifiée par `tests/test_site_build.py:test_ethics_warning_on_every_html_page`.
- UI Streamlit : composant `ethics_banner.render()` appelé en tête de chaque page.
- Tous les schémas JSON publiables incluent une note `description` qui réitère l'avertissement.

## 2. Audience cible et restrictions d'usage

### 2.1 Audience cible

- **Chercheurs en sciences sociales** : sociologues, politologues, anthropologues souhaitant explorer la géométrie civilisationnelle.
- **Praticiens méthodologues** : statisticiens, data scientists souhaitant auditer une approche hybride Huntington-IW-Hofstede.
- **Relecteurs externes** invités à challenger la méthodologie publiquement.

### 2.2 Usages autorisés

- Recherche académique citant `cvs/` avec attribution complète.
- Pédagogie sur la mesure transculturelle, ses limites, ses biais.
- Audit méthodologique externe.

### 2.3 Usages **interdits**

- **Profilage d'individus** : aucune inférence sur un individu réel à partir de son ISO3 d'appartenance, de son nom, de son patronyme, ou de toute caractéristique personnelle.
- **Récits identitaires ou de fracture** : le scoring ne doit pas alimenter des discours de « clash of civilizations » ou de hiérarchie civilisationnelle.
- **Décisions opérationnelles à conséquence individuelle** : immigration, embauche, octroi de visa, traitement administratif différencié — aucun usage du scoring n'est légitime dans ces contextes.
- **Reproduction commerciale** sans autorisation préalable, et **redistribution** des géométries GADM (interdite par la licence GADM ; cvs/ ne publie que Natural Earth + geoBoundaries).
- **Inférence ethnique ou religieuse à partir d'un nom** ou d'un patronyme.
- **Reconstruction d'identités** à partir de données ouvertes croisées.

## 3. Sources, licences, consent

| Source | Licence | Population enquêtée | Consent |
|---|---|---|---|
| Huntington (1996) | Copyright — citation académique uniquement | — | — |
| Inglehart & Welzel (2005, 2010) | Académique | — (théorie) | — |
| World Values Survey wave 7 | CC-BY 4.0 | Échantillons par pays, ~1500-3000 personnes / pays | Consent informé des enquêtés conforme aux protocoles WVS |
| Hofstede et al. (2010) | Citation académique autorisée | Travailleurs IBM (1967-1973), populations multinationales étendues | Pas de consent individuel — usage agrégé |
| Natural Earth | Domaine public | — | — |
| geoBoundaries | CC-BY 4.0 | — | — |
| Pew Religious Composition | Citation académique | Enquêtes nationales avec consent | Consent informé |
| WGI | CC-BY 4.0 | Méta-évaluation institutionnelle | — |
| FSI | Méthodologie publique | Méta-évaluation institutionnelle | — |

Notes :

- WVS publie des **données agrégées par pays** issues d'échantillons probabilistes. Aucun individu n'est identifiable.
- Hofstede travaille sur des **moyennes nationales** dérivées d'enquêtes IBM — les questions originales ne sont pas publiées par enquêté.

## 4. Légitimité de la classification des États

Le projet ne **classe** pas les États en civilisations. Il leur attribue un **vecteur continu d'affinité** `wₛ ∈ Δ¹⁰`. La « civilisation dominante par argmax » est un **résumé visualisable**, pas une étiquette identitaire.

Néanmoins, la pratique de représenter une géopolitique en termes civilisationnels est elle-même contestée (cf. [doc 11 — Critiques §A1, E19](11_critiques_and_responses.md)). Nous **assumons** cette limite :

- La représentation civilisationnelle n'est qu'**une grille de lecture parmi d'autres** (économie politique, géographie, religion, classes sociales).
- Elle ne **prédit pas** les conflits, les alignements, les politiques.
- Elle ne **justifie pas** des hiérarchies ou des prédestinations.

## 5. Modélisation interne des États : limite assumée

`cvs/` modélise un État comme un point `xₛ^score` dans `B_score`. Cette modélisation **ne capture pas** :

- Les **fractures internes** (urbain/rural, classes, religion, langue, immigration).
- L'**hétérogénéité régionale** sub-nationale.
- L'**évolution temporelle** des valeurs (le scoring est figé sur la wave 7 de WVS).
- Les **populations diasporiques** dispersées hors de leur État d'origine.

L'anticipation ADM1 (cf. [doc 04](04_adm1_preparation_policy.md)) prépare l'extension sub-nationale, mais aucune version active n'est publiée en v3.0.

## 6. Gouvernance des modifications

### 6.1 Versioning

- Toute modification d'un centroïde `μᵢ`, d'une liste d'États archétypes, d'une bibliographie, ou d'un poids éditorial **doit** être consignée dans `CHANGELOG.md avec date, motif, et auteur.
- Une modification **majeure** de la taxonomie (ajout/retrait d'une civilisation, redéfinition d'axe) impose un **bump de version majeur** (`x.0.0`) et une note de migration.
- Les versions sont publiées via Git tags. La v3.0 est documentée comme la première version corrigée des critiques de la v2.0.

### 6.2 Mécanisme de relecture

- Les **issues GitHub** sur `s-geffroy/cvs` sont le canal principal de remontée. Tout relecteur peut ouvrir une issue typée `methodology`, `data`, `ethics`, ou `code`.
- Une **PR** est requise pour toute modification substantielle. Les changements méthodologiques nécessitent une discussion préalable.
- La page « Relecture » du site publié donne les consignes : <https://s-geffroy.github.io/cvs/review/>.

### 6.3 Mécanisme de retrait

Si un usage **manifestement contraire** aux interdictions de §2.3 est détecté :

1. Notification publique sur le canal GitHub Discussions.
2. **Renforcement** des avertissements sur les pages concernées.
3. **Retrait temporaire** des artefacts (`/states/`, `/map/`, `/distances/`) si nécessaire, en conservant les pages méthodologiques.
4. **Révision de la politique** d'accès si l'incident persiste.

## 7. Conflits d'intérêt et indépendance

- L'auteur (`s-geffroy`) déclare **n'avoir aucun lien financier** avec Pew Research, World Bank, Fund For Peace, ou Hofstede Insights.
- Aucun financement institutionnel n'a été reçu pour ce projet à la date de v3.0.
- Le projet est publié **sous licence MIT** pour le code, **CC-BY 4.0** pour la documentation et les artefacts dérivés (à l'exception des géométries GADM, interdites).

## 8. Règles d'inférence interdites — liste explicite

Aucune des règles ci-dessous n'est implémentée ni autorisée par `cvs/` :

- Nom → religion (par exemple, déduire que « Mohamed » indique l'islam).
- Patronyme → ethnicité.
- Nom → civilisation.
- Adresse postale → religion ou civilisation.
- Téléphone, IP → localisation civilisationnelle d'une personne.
- Graphe social privé → caractérisation civilisationnelle.
- ISO3 d'origine d'un individu → vecteur d'affinité personnelle.

Toute personne demandant l'ajout d'une telle règle est explicitement priée de **se diriger ailleurs**.

## 9. Mise à jour et révision de cette politique

Cette politique est elle-même versionnée. La v3.0 (2026-06-01) étoffe la v2.0 (2026-05-30) suite aux critiques anticipées en [doc 11 §E18](11_critiques_and_responses.md). Toute future révision sera consignée ici en tête.

---

| Version | Date | Modification |
|---|---|---|
| v3.0 | 2026-06-01 | Étoffement complet : audience, usages interdits, sources/licences/consent, gouvernance, retrait, conflits d'intérêt, règles interdites explicites. |
| v2.0 | 2026-05-30 | Version initiale 8 lignes. Insuffisante (cf. [doc 11 §E18](11_critiques_and_responses.md)). |
