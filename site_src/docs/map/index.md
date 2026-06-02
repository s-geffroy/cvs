# Carte interactive

!!! warning "Avertissement éthique"
    Ce profil est inféré à partir de sources publiques agrégées. Il ne doit pas être utilisé pour classer des individus réels.

!!! danger "Restrictions de représentation"
    - Aucune géométrie **GADM** n'est publiée (cf. [politique ADM1](../adm1_policy.md)).
    - Frontières issues de **Natural Earth 110m** (domaine public), simplification globale —
      certains États (HKG, SGP) sont absents à cette résolution. Antarctique exclu.
    - La couleur d'un État reflète sa **civilisation curatée** depuis la taxonomie
      lorsque disponible, sinon l'**argmax du vecteur d'affinité** en `B_score`. Elle
      **ne représente pas une identité** des populations.

<div id="civvec-map-mode" role="radiogroup" aria-label="Mode de coloration" style="margin-bottom: 0.5rem; font-size: 0.9rem;">
  <label style="margin-right: 1rem;"><input type="radio" name="civvec-map-mode" value="macro" checked> Macro civilisation</label>
  <label><input type="radio" name="civvec-map-mode" value="sub"> Sous-ensemble</label>
</div>
<div id="civvec-map" style="width: 100%; height: 560px; border: 1px solid var(--md-default-fg-color--lightest);"></div>
<div id="civvec-map-legend" style="margin-top: 0.75rem; font-size: 0.85rem;"></div>

<noscript>
La carte interactive nécessite JavaScript. Les artefacts sources restent
téléchargeables :
[`global_state_baseline.geojson`](../assets/data/global_state_baseline.geojson) ·
[`state_coordinates.json`](../assets/data/state_coordinates.json) ·
[`civilization_centroids.json`](../assets/data/civilization_centroids.json).
</noscript>

## Détails techniques

- **Moteur** : [MapLibre GL JS](https://maplibre.org/) 4.7.1 via CDN pinné.
- **Projection** : Mercator par défaut, basemap absente (pas de tuiles externes).
- **Couches** : choropleth par civilisation curatée (taxonomie) avec repli sur
  l'argmax du vecteur d'affinité ; bordures sur tous les États ; mode
  sous-ensemble en variation HSL de la couleur parente.
- **Source géométries** : `ne_110m_admin_0_countries` @ commit `ca96624a56bd078437bca8184e78163e5039ad19` — collection complète (Antarctique exclu).

## Téléchargements

- [`global_state_baseline.geojson`](../assets/data/global_state_baseline.geojson)
- [`state_coordinates.json`](../assets/data/state_coordinates.json)
- [`civilization_centroids.json`](../assets/data/civilization_centroids.json)

---

[Liste des États](../states/index.md) ·
[Base vectorielle B_vec](../basis/index.md)
