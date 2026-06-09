/*
 * civvec — Carte interactive
 *
 * MapLibre GL JS — choropleth des États souverains coloriés en deux modes :
 *  - Macro (par défaut) : civilisation curatée depuis la taxonomie quand
 *    disponible, sinon argmax du vecteur d'affinité en B_score.
 *  - Sous-ensemble : variation HSL de la couleur parente selon le sub_cluster
 *    (anglo, catholic_europe, arab_islamic, ...) déclaré dans la taxonomie.
 *
 * Aucun appel à un fond de carte externe : seuls les polygones Natural Earth
 * 110m sont rendus, avec bordures sur tous les pays (Antarctique exclu).
 */
(function initCivvecMap() {
  const mapContainerSelector = '#civvec-map';
  const legendContainerSelector = '#civvec-map-legend';
  const modeContainerSelector = '#civvec-map-mode';
  if (!document.querySelector(mapContainerSelector)) {
    return;
  }
  if (typeof maplibregl === 'undefined') {
    console.warn('[civvec/map] MapLibre GL JS non chargé — abandon.');
    return;
  }

  const civilizationColorPalette = {
    western: '#1f77b4',
    orthodox: '#9467bd',
    islamic: '#2ca02c',
    sinic: '#d62728',
    hindic: '#ff7f0e',
    japanese: '#e377c2',
    buddhist: '#bcbd22',
    latin_american: '#17becf',
    african: '#8c564b',
    indigenous: '#7f7f7f',
    oceanian: '#aec7e8'
  };
  const fallbackColor = '#cccccc';

  const provenanceColorPalette = {
    observed: '#08519c',
    observed_with_dim_imputation: '#3182bd',
    imputed_wvs_items: '#6baed6',
    imputed_pew: '#fdae6b',
    imputed_governance: '#e6550d',
    centroid_prior: '#bdbdbd',
    unresolved: fallbackColor
  };

  const provenanceLabels = {
    observed: 'observé (sondage direct)',
    observed_with_dim_imputation: 'observé (dimensions partiellement imputées)',
    imputed_wvs_items: 'prédit depuis items WVS (waves 5-6, ridge sur wave-7)',
    imputed_pew: 'imputé via Pew + UNDP + UN voting + V-Dem → IW',
    imputed_governance: 'imputé via WGI + FSI + UNDP + UN voting + V-Dem → Hofstede',
    centroid_prior: 'prior centroïde civilisationnel',
    unresolved: 'non résolu'
  };

  // Labels longs des composantes du champ continu (Inglehart-Welzel + Hofstede
  // + 3 indicateurs synthétiques agrégés) — utilisés dans le sélecteur, la
  // légende et le bandeau de lecture.
  const componentLabels = {
    civ_identity_sharpness: 'Force d’identité civilisationnelle',
    civ_texture_intensity: 'Tension culturelle locale (tr G)',
    civ_classification_margin: 'Profondeur du cœur civilisationnel (marge)',
    x_viz_ts: 'Inglehart — TS · Traditionnel ↔ Séculier-rationnel',
    x_viz_se: 'Inglehart — SE · Survie ↔ Expression de soi',
    x_score_pdi: 'Hofstede — PDI · Distance hiérarchique',
    x_score_idv: 'Hofstede — IDV · Individualisme vs Collectivisme',
    x_score_mas: 'Hofstede — MAS · Masculinité vs Féminité',
    x_score_uai: 'Hofstede — UAI · Évitement de l’incertitude',
    x_score_lto: 'Hofstede — LTO · Orientation long terme',
    x_score_ivr: 'Hofstede — IVR · Indulgence vs Retenue'
  };

  // Labels parlants pour la métrique du champ continu.
  const metricLabels = {
    mean: 'Valeur — où se situent les sociétés sur cet axe ?',
    grad_magnitude: 'Transition — où le changement est-il le plus rapide ?'
  };

  // Groupement du sélecteur Composante selon le régime de lecture.
  const READ_MODE_GROUP_LABEL = {
    paired: 'Indicateurs synthétiques (à lire ensemble)',
    standalone: 'Indicateur synthétique autonome',
    raw: 'Composantes brutes (axes culturels)'
  };
  const READ_MODE_GROUP_ORDER = ['paired', 'standalone', 'raw'];

  // Cache mémoire des images partenaires pour swap instantané.
  const preloadedRasterImages = new Map();

  const provenanceOpacity = {
    observed: 0.82,
    observed_with_dim_imputation: 0.72,
    imputed_wvs_items: 0.72,
    imputed_pew: 0.62,
    imputed_governance: 0.62,
    centroid_prior: 0.42,
    unresolved: 0.25
  };

  function effectiveProvenance(stateEntry) {
    if (!stateEntry || !stateEntry.data_quality) {
      return 'unresolved';
    }
    const vizProvenance = stateEntry.data_quality.x_viz_provenance;
    const scoreProvenance = stateEntry.data_quality.x_score_provenance;
    const tierRanking = [
      'centroid_prior',
      'imputed_pew',
      'imputed_governance',
      'observed_with_dim_imputation',
      'observed'
    ];
    let worstSeen = null;
    let worstRank = tierRanking.length;
    for (const candidate of [vizProvenance, scoreProvenance]) {
      const rank = tierRanking.indexOf(candidate);
      if (rank !== -1 && rank < worstRank) {
        worstRank = rank;
        worstSeen = candidate;
      }
    }
    return worstSeen || 'unresolved';
  }

  let currentDisplayMode = 'macro';
  const subClusterRegistry = new Map();

  async function fetchJson(relativeUrl) {
    const response = await fetch(relativeUrl);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status} pour ${relativeUrl}`);
    }
    return response.json();
  }

  function dominantCivilizationByAffinity(affinityVector) {
    let bestCivilization = null;
    let bestWeight = -Infinity;
    for (const [civilizationId, weight] of Object.entries(affinityVector || {})) {
      if (weight > bestWeight) {
        bestWeight = weight;
        bestCivilization = civilizationId;
      }
    }
    return { civilizationId: bestCivilization, weight: bestWeight };
  }

  function indexStateCoordinatesByIso3(stateCoordinatesPayload) {
    const result = {};
    for (const stateEntry of stateCoordinatesPayload.states) {
      result[stateEntry.iso3] = stateEntry;
    }
    return result;
  }

  function hexToRgb(hexColor) {
    const normalized = hexColor.replace('#', '');
    return {
      red: parseInt(normalized.substring(0, 2), 16),
      green: parseInt(normalized.substring(2, 4), 16),
      blue: parseInt(normalized.substring(4, 6), 16)
    };
  }

  function rgbToHsl(red, green, blue) {
    const redNorm = red / 255;
    const greenNorm = green / 255;
    const blueNorm = blue / 255;
    const maxChannel = Math.max(redNorm, greenNorm, blueNorm);
    const minChannel = Math.min(redNorm, greenNorm, blueNorm);
    const lightness = (maxChannel + minChannel) / 2;
    let hue = 0;
    let saturation = 0;
    if (maxChannel !== minChannel) {
      const delta = maxChannel - minChannel;
      saturation = lightness > 0.5 ? delta / (2 - maxChannel - minChannel) : delta / (maxChannel + minChannel);
      switch (maxChannel) {
        case redNorm:
          hue = ((greenNorm - blueNorm) / delta + (greenNorm < blueNorm ? 6 : 0)) * 60;
          break;
        case greenNorm:
          hue = ((blueNorm - redNorm) / delta + 2) * 60;
          break;
        default:
          hue = ((redNorm - greenNorm) / delta + 4) * 60;
      }
    }
    return { hue, saturation, lightness };
  }

  function hslToHex(hue, saturation, lightness) {
    const chroma = (1 - Math.abs(2 * lightness - 1)) * saturation;
    const huePrime = hue / 60;
    const secondComponent = chroma * (1 - Math.abs((huePrime % 2) - 1));
    let redBase = 0;
    let greenBase = 0;
    let blueBase = 0;
    if (huePrime >= 0 && huePrime < 1) {
      redBase = chroma;
      greenBase = secondComponent;
    } else if (huePrime < 2) {
      redBase = secondComponent;
      greenBase = chroma;
    } else if (huePrime < 3) {
      greenBase = chroma;
      blueBase = secondComponent;
    } else if (huePrime < 4) {
      greenBase = secondComponent;
      blueBase = chroma;
    } else if (huePrime < 5) {
      redBase = secondComponent;
      blueBase = chroma;
    } else {
      redBase = chroma;
      blueBase = secondComponent;
    }
    const offset = lightness - chroma / 2;
    const toHex = (component) =>
      Math.round((component + offset) * 255)
        .toString(16)
        .padStart(2, '0');
    return `#${toHex(redBase)}${toHex(greenBase)}${toHex(blueBase)}`;
  }

  function hashSubClusterId(subClusterId) {
    let hash = 0;
    for (let index = 0; index < subClusterId.length; index += 1) {
      hash = (hash * 31 + subClusterId.charCodeAt(index)) | 0;
    }
    return hash;
  }

  function deriveHslShade(parentHexColor, subClusterId) {
    if (!parentHexColor || !subClusterId) {
      return null;
    }
    const { red, green, blue } = hexToRgb(parentHexColor);
    const { hue, saturation, lightness } = rgbToHsl(red, green, blue);
    const seed = hashSubClusterId(subClusterId);
    const lightnessOffset = (((seed % 7) - 3) / 3) * 0.15;
    const adjustedLightness = Math.max(0.15, Math.min(0.85, lightness + lightnessOffset));
    return hslToHex(hue, saturation, adjustedLightness);
  }

  function decorateFeaturesWithMembership(geojsonCollection, stateCoordinatesByIso3) {
    for (const feature of geojsonCollection.features) {
      const iso3 = feature.properties.iso3;
      const stateEntry = stateCoordinatesByIso3[iso3];
      if (!stateEntry) {
        feature.properties.curated_civilization = null;
        feature.properties.affinity_top_civilization = null;
        feature.properties.affinity_top_weight = null;
        feature.properties.effective_civilization = null;
        feature.properties.effective_origin = 'missing';
        feature.properties.sub_cluster_id = null;
        feature.properties.sub_cluster_label = null;
        feature.properties.fill_color_macro = fallbackColor;
        feature.properties.fill_color_sub = fallbackColor;
        feature.properties.fill_color_provenance = fallbackColor;
        feature.properties.x_viz_provenance = 'unresolved';
        feature.properties.x_score_provenance = 'unresolved';
        feature.properties.effective_provenance = 'unresolved';
        feature.properties.fill_opacity = provenanceOpacity.unresolved;
        continue;
      }
      const argmax = dominantCivilizationByAffinity(stateEntry.affinity_vector);
      const curatedCivilization = stateEntry.curated_civilization || null;
      const fallbackCivilization =
        (stateEntry.data_quality && stateEntry.data_quality.fallback_civilization_id) || null;
      const effectiveCivilization =
        curatedCivilization || fallbackCivilization || argmax.civilizationId;
      const effectiveOrigin = curatedCivilization
        ? 'curated'
        : fallbackCivilization
          ? 'fallback'
          : 'affinity';
      const subClusterId = stateEntry.sub_cluster_id || null;
      const subClusterLabel = stateEntry.sub_cluster_label || null;
      const fillColorMacro =
        civilizationColorPalette[effectiveCivilization] || fallbackColor;
      const fillColorSub = subClusterId
        ? deriveHslShade(fillColorMacro, subClusterId) || fillColorMacro
        : fillColorMacro;

      if (subClusterId && !subClusterRegistry.has(subClusterId)) {
        subClusterRegistry.set(subClusterId, {
          subClusterId,
          subClusterLabel,
          parentCivilization: effectiveCivilization,
          parentColor: fillColorMacro,
          shadeColor: fillColorSub
        });
      }

      const stateProvenance = effectiveProvenance(stateEntry);
      const fillColorProvenance =
        provenanceColorPalette[stateProvenance] || fallbackColor;
      const fillOpacity =
        provenanceOpacity[stateProvenance] !== undefined
          ? provenanceOpacity[stateProvenance]
          : 0.78;

      feature.properties.curated_civilization = curatedCivilization;
      feature.properties.curated_role = stateEntry.curated_role || null;
      feature.properties.affinity_top_civilization = argmax.civilizationId;
      feature.properties.affinity_top_weight = argmax.weight;
      feature.properties.effective_civilization = effectiveCivilization;
      feature.properties.effective_origin = effectiveOrigin;
      feature.properties.sub_cluster_id = subClusterId;
      feature.properties.sub_cluster_label = subClusterLabel;
      feature.properties.fill_color_macro = fillColorMacro;
      feature.properties.fill_color_sub = fillColorSub;
      feature.properties.fill_color_provenance = fillColorProvenance;
      feature.properties.x_viz_provenance =
        (stateEntry.data_quality && stateEntry.data_quality.x_viz_provenance) || 'unresolved';
      feature.properties.x_score_provenance =
        (stateEntry.data_quality && stateEntry.data_quality.x_score_provenance) || 'unresolved';
      feature.properties.effective_provenance = stateProvenance;
      feature.properties.fill_opacity = fillOpacity;
      feature.properties.fallback_civilization_id =
        (stateEntry.data_quality && stateEntry.data_quality.fallback_civilization_id) || null;
    }
    return geojsonCollection;
  }

  function escapeHtml(rawString) {
    if (rawString === null || rawString === undefined) {
      return '';
    }
    return String(rawString)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function buildLegend(legendContainer, mode) {
    if (mode === 'plates') {
      const manifest = platesManifest();
      const civColorRow = Object.entries(civilizationColorPalette)
        .map(
          ([civilizationId, color]) =>
            `<span style="display:inline-block;width:0.95em;height:0.95em;background:${color};margin-right:0.3em;vertical-align:middle;border:1px solid #999;"></span>${civilizationId}`
        )
        .join(' &nbsp; ');
      const description = manifest && manifest.description_fr ? manifest.description_fr : '';
      legendContainer.innerHTML = `
<strong>Légende — Plaques &amp; Failles (Huntington-style)</strong><br/>
<div style="margin-top:0.4em; font-size:0.92em;">
  <strong>Plaques</strong> — argmax du vecteur d'affinité GP par cellule 1° (catégoriel) :<br/>
  ${civColorRow}
</div>
<div style="margin-top:0.5em; font-size:0.9em;">
  <strong>Failles</strong> — frontières dures entre cellules d'argmax différents. <br/>
  Épaisseur ∝ <code>friction = (margin_A + margin_B)/2 · distance_culturelle</code>.<br/>
  Opacité ∝ <code>confidence = 1 − var_GP / var_max</code>. Couleur = paire civilisationnelle (moyenne RGB).
</div>
<div style="margin-top:0.5em; font-size:0.9em;">
  <span style="display:inline-block;width:0.8em;height:0.8em;background:#222;border-radius:50%;margin-right:0.3em;vertical-align:middle;"></span> Chevrons directionnels &nbsp;
  <span style="display:inline-block;width:0.95em;height:0.95em;background:#ffd400;border:1px solid #222;border-radius:50%;margin-right:0.3em;vertical-align:middle;"></span> Triple junction (3+ civs au coin) &nbsp;
  <span style="display:inline-block;width:0.95em;height:0.95em;background:#ff5577;border:1px solid #fff;border-radius:50%;margin-right:0.3em;vertical-align:middle;"></span> Enclave
</div>
<div style="margin-top:0.5em; font-size:0.9em;">
  <span style="display:inline-block;width:0.95em;height:0.95em;background:repeating-linear-gradient(45deg,#666 0 3px,#bbb 3px 6px);margin-right:0.3em;vertical-align:middle;"></span> Trame grise = variance GP &gt; 90<sup>e</sup> percentile (zones hallucinées par le GP).
</div>
<div style="margin-top:0.5em; font-size:0.85em;">
  <em>${escapeHtml(description)}</em>
  Voir <a href="../methodology/17_continuous_field/">doc 17 §5</a>.
</div>`;
      return;
    }
    if (mode === 'continuous') {
      const matchedRaster = continuousFieldIndex && continuousFieldIndex.rasters
        ? continuousFieldIndex.rasters.find(
            (raster) =>
              raster.component === currentContinuousField.component &&
              raster.metric === currentContinuousField.metric
          )
        : null;
      if (!matchedRaster) {
        legendContainer.innerHTML =
          '<em>Champ continu indisponible — raster manquant.</em>';
        return;
      }
      const colormapKeyToLabel = {
        RdBu_r: 'Rouge ↔ Bleu (échelle signée)',
        plasma: 'Plasma (magnitude)'
      };
      const componentLabel =
        componentLabels[matchedRaster.component] || matchedRaster.component;
      const metricLabel = metricLabels[matchedRaster.metric] || matchedRaster.metric;
      legendContainer.innerHTML = `
<strong>Légende — champ continu (cascade ⇒ Gaussian Process)</strong><br/>
<div style="margin-top:0.3em; font-size:0.95em;">
  <strong>${escapeHtml(componentLabel)}</strong><br/>
  <em>${escapeHtml(metricLabel)}</em><br/>
  <small>Code : <code>${escapeHtml(matchedRaster.component)}</code> / <code>${escapeHtml(matchedRaster.metric)}</code></small><br/>
  Plage : <code>[${matchedRaster.value_min.toFixed(2)}, ${matchedRaster.value_max.toFixed(2)}]</code><br/>
  Palette : ${colormapKeyToLabel[matchedRaster.colormap] || matchedRaster.colormap}<br/>
  <em>${escapeHtml(matchedRaster.description_fr)}</em>
</div>
<div style="margin-top:0.4em; font-size:0.85em;">
  Le champ est interpolé par un GP Matérn 3/2 sphérique à partir de
  237 sample points (centroïdes de population par État). Cf.
  <a href="../methodology/17_continuous_field/">doc 17</a>.
</div>`;
      return;
    }
    if (mode === 'provenance') {
      const parts = [
        '<strong>Légende — provenance des coordonnées (cascade d\'imputation)</strong><br/>',
        '<div style="margin-top:0.3em; font-size: 0.95em;">'
      ];
      for (const tier of Object.keys(provenanceColorPalette)) {
        const color = provenanceColorPalette[tier];
        const opacity = provenanceOpacity[tier] !== undefined ? provenanceOpacity[tier] : 1;
        const label = provenanceLabels[tier];
        parts.push(
          `<div style="margin:0.15em 0;"><span style="display:inline-block;width:1.1em;height:1.1em;background:${color};opacity:${opacity};margin-right:0.4em;vertical-align:middle;border:1px solid #999;"></span><code>${tier}</code> — ${label}</div>`
        );
      }
      parts.push('</div>');
      parts.push(
        '<div style="margin-top:0.4em; font-size: 0.85em;">L\'opacité reflète aussi le tier : les États non observés sont volontairement <em>estompés</em>. Cf. <a href="../methodology/16_imputation_cascade/">doc 16</a>.</div>'
      );
      legendContainer.innerHTML = parts.join('');
      return;
    }
    if (mode === 'sub') {
      const grouped = new Map();
      for (const entry of subClusterRegistry.values()) {
        if (!grouped.has(entry.parentCivilization)) {
          grouped.set(entry.parentCivilization, []);
        }
        grouped.get(entry.parentCivilization).push(entry);
      }
      const parts = [
        '<strong>Légende — sous-ensemble civilisationnel</strong><br/>'
      ];
      for (const civilizationId of Object.keys(civilizationColorPalette)) {
        const entries = grouped.get(civilizationId);
        if (!entries || entries.length === 0) {
          continue;
        }
        const parentSwatch = `<span style="display:inline-block;width:0.9em;height:0.9em;background:${civilizationColorPalette[civilizationId]};margin-right:0.3em;vertical-align:middle;"></span>`;
        const subSwatches = entries
          .map(
            (entry) =>
              `<span style="display:inline-block;width:0.9em;height:0.9em;background:${entry.shadeColor};margin:0 0.3em;vertical-align:middle;border:1px solid #999;"></span>${entry.subClusterLabel || entry.subClusterId}`
          )
          .join(' &nbsp; ');
        parts.push(`<div style="margin:0.15em 0;">${parentSwatch}<em>${civilizationId}</em> &nbsp; ${subSwatches}</div>`);
      }
      parts.push(
        `<div style="margin-top:0.4em;"><span style="display:inline-block;width:0.9em;height:0.9em;background:${fallbackColor};margin-right:0.3em;vertical-align:middle;"></span>Pas de données / hors taxonomie</div>`
      );
      legendContainer.innerHTML = parts.join('');
      return;
    }
    legendContainer.innerHTML =
      '<strong>Légende — civilisation dominante (curatée &gt; affinité)</strong><br/>' +
      Object.entries(civilizationColorPalette)
        .map(
          ([civilizationId, color]) =>
            `<span style="display:inline-block;width:0.9em;height:0.9em;background:${color};margin-right:0.3em;vertical-align:middle;"></span>${civilizationId}`
        )
        .join(' &nbsp; ') +
      ` &nbsp; <span style="display:inline-block;width:0.9em;height:0.9em;background:${fallbackColor};margin-right:0.3em;vertical-align:middle;"></span>Pas de données / hors taxonomie`;
  }

  let continuousFieldIndex = null;
  let currentContinuousField = { component: 'x_viz_ts', metric: 'mean' };

  // Plates & Faults — état des toggles secondaires (couches optionnelles).
  const platesLayerToggleState = {
    contested_margin: false,
    chevrons: true,
    triple_junctions: true,
    enclaves: true,
    uncertainty_mask: true
  };

  const civPairColorPalette = {};

  function platesManifest() {
    return (continuousFieldIndex && continuousFieldIndex.plates_and_faults) || null;
  }

  // Injecte dynamiquement la radio « Plaques & Failles » et son rang de
  // toggles secondaires, sans toucher au markdown de la page (le mode
  // peut donc être activé/désactivé via la simple présence du manifest
  // dans index.json — pas d'édition de la page nécessaire).
  function injectPlatesModeControls() {
    if (!platesManifest()) return;
    const modeContainer = document.querySelector(modeContainerSelector);
    if (modeContainer && !modeContainer.querySelector('input[value="plates"]')) {
      const platesLabel = document.createElement('label');
      platesLabel.style.marginRight = '1rem';
      platesLabel.title =
        'Cartographie catégorielle Huntington-style : plaques par argmax du vecteur d’affinité, failles vectorielles, zones contestées, masque d’incertitude.';
      platesLabel.innerHTML =
        '<input type="radio" name="civvec-map-mode" value="plates"> Plaques &amp; Failles';
      const continuousRadioLabel = modeContainer.querySelector(
        'input[value="continuous"]'
      );
      if (continuousRadioLabel) {
        modeContainer.insertBefore(platesLabel, continuousRadioLabel.parentElement);
        const continuousInput = modeContainer.querySelector('input[value="continuous"]');
        if (continuousInput && !continuousInput.dataset.platesRenamed) {
          const parentLabel = continuousInput.parentElement;
          if (parentLabel) {
            parentLabel.childNodes.forEach((childNode) => {
              if (childNode.nodeType === Node.TEXT_NODE) {
                childNode.textContent = ' Champ continu (GP, vue brute)';
              }
            });
          }
          continuousInput.dataset.platesRenamed = '1';
        }
      } else {
        modeContainer.appendChild(platesLabel);
      }
    }
    if (!document.querySelector('#civvec-map-plates-toggles')) {
      const togglesContainer = document.createElement('div');
      togglesContainer.id = 'civvec-map-plates-toggles';
      togglesContainer.style.display = 'none';
      togglesContainer.style.gap = '1rem';
      togglesContainer.style.flexWrap = 'wrap';
      togglesContainer.style.margin = '0 0 0.4rem 0';
      togglesContainer.style.fontSize = '0.88rem';
      const toggleSpecifications = [
        {
          layerKey: 'contested_margin',
          label: 'Marges contestées',
          title:
            "Choropleth divergent : zones où top1 − top2 du vecteur d'affinité est faible (= deux civilisations comparables, = contestée)."
        },
        {
          layerKey: 'chevrons',
          label: 'Chevrons directionnels',
          title:
            'Petits points orientés sur les failles : pointent du côté moins décisif vers le côté plus décisif.'
        },
        {
          layerKey: 'triple_junctions',
          label: 'Triple junctions',
          title:
            'Coins 2×2 où trois civilisations ou plus se rencontrent (Caucase, Sahel, Asie centrale).'
        },
        {
          layerKey: 'enclaves',
          label: 'Enclaves',
          title:
            "Étoiles sur les cellules dont l'argmax diffère de leurs 8 voisines (diasporas, micro-États culturels)."
        },
        {
          layerKey: 'uncertainty_mask',
          label: "Masque d'incertitude",
          title:
            'Trame grise sur les cellules dont la variance GP dépasse le 90e percentile (zones hallucinées par le GP).'
        }
      ];
      for (const specification of toggleSpecifications) {
        const label = document.createElement('label');
        label.title = specification.title;
        const checkboxInput = document.createElement('input');
        checkboxInput.type = 'checkbox';
        checkboxInput.dataset.platesLayer = specification.layerKey;
        checkboxInput.checked = !!platesLayerToggleState[specification.layerKey];
        label.appendChild(checkboxInput);
        label.appendChild(document.createTextNode(' ' + specification.label));
        togglesContainer.appendChild(label);
      }
      if (modeContainer && modeContainer.parentNode) {
        modeContainer.parentNode.insertBefore(
          togglesContainer,
          modeContainer.nextSibling
        );
      } else {
        document.body.appendChild(togglesContainer);
      }
    }
  }

  function platesRasterFilename(role) {
    const manifest = platesManifest();
    if (!manifest) return null;
    const record = (manifest.rasters || []).find((entry) => entry.role === role);
    return record ? record.filename : null;
  }

  function platesVectorFilename(role) {
    const manifest = platesManifest();
    if (!manifest) return null;
    const record = (manifest.vector_layers || []).find(
      (entry) => entry.role === role
    );
    return record ? record.filename : null;
  }

  function civPairColor(civPair) {
    if (civPairColorPalette[civPair]) return civPairColorPalette[civPair];
    const [lowCiv, highCiv] = civPair.split('__');
    const lowColor = civilizationColorPalette[lowCiv] || fallbackColor;
    const highColor = civilizationColorPalette[highCiv] || fallbackColor;
    const lowRgb = hexToRgb(lowColor);
    const highRgb = hexToRgb(highColor);
    const mixedColor =
      '#' +
      [
        Math.round((lowRgb.red + highRgb.red) / 2),
        Math.round((lowRgb.green + highRgb.green) / 2),
        Math.round((lowRgb.blue + highRgb.blue) / 2)
      ]
        .map((channel) => channel.toString(16).padStart(2, '0'))
        .join('');
    civPairColorPalette[civPair] = mixedColor;
    return mixedColor;
  }

  const platesRasterCoordinates = () => {
    const WEB_MERCATOR_LATITUDE_BOUND_DEG = 85.0511;
    const bboxRaw =
      (continuousFieldIndex && continuousFieldIndex.bbox) || {
        longitude_min_deg: -180,
        longitude_max_deg: 180,
        latitude_min_deg: -90,
        latitude_max_deg: 90
      };
    const clampLatitude = (latitude) =>
      Math.max(
        -WEB_MERCATOR_LATITUDE_BOUND_DEG,
        Math.min(WEB_MERCATOR_LATITUDE_BOUND_DEG, latitude)
      );
    return [
      [bboxRaw.longitude_min_deg, clampLatitude(bboxRaw.latitude_max_deg)],
      [bboxRaw.longitude_max_deg, clampLatitude(bboxRaw.latitude_max_deg)],
      [bboxRaw.longitude_max_deg, clampLatitude(bboxRaw.latitude_min_deg)],
      [bboxRaw.longitude_min_deg, clampLatitude(bboxRaw.latitude_min_deg)]
    ];
  };

  function ensurePlatesRasterLayer(map, sourceId, layerId, role, opacity, beforeLayerId) {
    const filename = platesRasterFilename(role);
    if (!filename) return;
    const rasterUrl = `../assets/data/continuous_field/${filename}`;
    const coordinates = platesRasterCoordinates();
    if (!map.getSource(sourceId)) {
      map.addSource(sourceId, { type: 'image', url: rasterUrl, coordinates });
    }
    if (!map.getLayer(layerId)) {
      map.addLayer(
        {
          id: layerId,
          source: sourceId,
          type: 'raster',
          paint: { 'raster-opacity': opacity }
        },
        beforeLayerId
      );
    }
  }

  async function ensurePlatesVectorLayer(map, sourceId, role) {
    const filename = platesVectorFilename(role);
    if (!filename) return false;
    if (!map.getSource(sourceId)) {
      try {
        const data = await fetchJson(
          `../assets/data/continuous_field/${filename}`
        );
        map.addSource(sourceId, { type: 'geojson', data });
      } catch (error) {
        console.warn(`[civvec/map] could not load ${role}`, error);
        return false;
      }
    }
    return true;
  }

  function platesFrictionRange() {
    const manifest = platesManifest();
    if (!manifest) return [0, 1];
    const faultsRecord = (manifest.vector_layers || []).find(
      (entry) => entry.role === 'faults'
    );
    if (!faultsRecord) return [0, 1];
    return [
      faultsRecord.friction_min || 0,
      Math.max(faultsRecord.friction_max || 1, 0.001)
    ];
  }

  async function applyPlatesMode(map) {
    if (!platesManifest()) {
      console.warn('[civvec/map] plates_and_faults manifest indisponible — index.json non régénéré ?');
      return;
    }
    if (map.getLayer('states-fill')) {
      map.setPaintProperty('states-fill', 'fill-opacity', 0.0);
    }
    if (map.getLayer('continuous-field-layer')) {
      map.setLayoutProperty('continuous-field-layer', 'visibility', 'none');
    }

    ensurePlatesRasterLayer(
      map,
      'plates-base-source',
      'plates-base-layer',
      'plates',
      0.85,
      'states-outline'
    );
    ensurePlatesRasterLayer(
      map,
      'plates-margin-source',
      'plates-margin-layer',
      'contested_margin',
      0.55,
      'states-outline'
    );
    ensurePlatesRasterLayer(
      map,
      'plates-mask-source',
      'plates-mask-layer',
      'uncertainty_mask',
      0.9,
      'states-outline'
    );

    if (await ensurePlatesVectorLayer(map, 'plates-faults-source', 'faults')) {
      if (!map.getLayer('plates-faults-layer')) {
        const [frictionMin, frictionMax] = platesFrictionRange();
        map.addLayer(
          {
            id: 'plates-faults-layer',
            source: 'plates-faults-source',
            type: 'line',
            paint: {
              'line-color': [
                'case',
                ['has', 'civ_pair'],
                ['get', 'civ_pair_color'],
                '#444444'
              ],
              'line-width': [
                'interpolate',
                ['linear'],
                ['get', 'friction'],
                frictionMin,
                0.6,
                frictionMax,
                4.0
              ],
              'line-opacity': [
                'interpolate',
                ['linear'],
                ['get', 'confidence'],
                0.0,
                0.25,
                1.0,
                0.95
              ]
            },
            layout: { 'line-cap': 'round', 'line-join': 'round' }
          },
          'states-outline'
        );
        annotateFaultColors(map);
      }
    }
    if (await ensurePlatesVectorLayer(map, 'plates-chevrons-source', 'chevrons')) {
      if (!map.getLayer('plates-chevrons-layer')) {
        map.addLayer(
          {
            id: 'plates-chevrons-layer',
            source: 'plates-chevrons-source',
            type: 'circle',
            paint: {
              'circle-radius': 2.2,
              'circle-color': '#222',
              'circle-stroke-color': '#fff',
              'circle-stroke-width': 0.7,
              'circle-opacity': 0.75
            }
          },
          'states-outline'
        );
      }
    }
    if (
      await ensurePlatesVectorLayer(
        map,
        'plates-triple-junctions-source',
        'triple_junctions'
      )
    ) {
      if (!map.getLayer('plates-triple-junctions-layer')) {
        map.addLayer(
          {
            id: 'plates-triple-junctions-layer',
            source: 'plates-triple-junctions-source',
            type: 'circle',
            paint: {
              'circle-radius': 4.2,
              'circle-color': '#ffd400',
              'circle-stroke-color': '#222',
              'circle-stroke-width': 1.0,
              'circle-opacity': 0.92
            }
          },
          'states-outline'
        );
      }
    }
    if (await ensurePlatesVectorLayer(map, 'plates-enclaves-source', 'enclaves')) {
      if (!map.getLayer('plates-enclaves-layer')) {
        map.addLayer(
          {
            id: 'plates-enclaves-layer',
            source: 'plates-enclaves-source',
            type: 'circle',
            paint: {
              'circle-radius': 5.0,
              'circle-color': '#ff5577',
              'circle-stroke-color': '#fff',
              'circle-stroke-width': 1.2,
              'circle-opacity': 0.88
            }
          },
          'states-outline'
        );
      }
    }

    refreshPlatesLayerVisibility(map);
  }

  function annotateFaultColors(map) {
    const sourceObject = map.getSource('plates-faults-source');
    if (!sourceObject) return;
    try {
      const data = sourceObject._data;
      if (!data || !data.features) return;
      for (const feature of data.features) {
        const civPair = feature.properties && feature.properties.civ_pair;
        if (civPair) {
          feature.properties.civ_pair_color = civPairColor(civPair);
        }
      }
      sourceObject.setData(data);
    } catch (error) {
      console.warn('[civvec/map] annotateFaultColors a échoué', error);
    }
  }

  function setLayerVisibility(map, layerId, visible) {
    if (!map.getLayer(layerId)) return;
    map.setLayoutProperty(layerId, 'visibility', visible ? 'visible' : 'none');
  }

  function refreshPlatesLayerVisibility(map) {
    if (currentDisplayMode !== 'plates') {
      for (const layerId of [
        'plates-base-layer',
        'plates-margin-layer',
        'plates-mask-layer',
        'plates-faults-layer',
        'plates-chevrons-layer',
        'plates-triple-junctions-layer',
        'plates-enclaves-layer'
      ]) {
        setLayerVisibility(map, layerId, false);
      }
      return;
    }
    setLayerVisibility(map, 'plates-base-layer', true);
    setLayerVisibility(map, 'plates-faults-layer', true);
    setLayerVisibility(
      map,
      'plates-margin-layer',
      platesLayerToggleState.contested_margin
    );
    setLayerVisibility(
      map,
      'plates-chevrons-layer',
      platesLayerToggleState.chevrons
    );
    setLayerVisibility(
      map,
      'plates-triple-junctions-layer',
      platesLayerToggleState.triple_junctions
    );
    setLayerVisibility(
      map,
      'plates-enclaves-layer',
      platesLayerToggleState.enclaves
    );
    setLayerVisibility(
      map,
      'plates-mask-layer',
      platesLayerToggleState.uncertainty_mask
    );
  }

  function rasterByComponentAndMetric(componentId, metricId) {
    if (!continuousFieldIndex || !continuousFieldIndex.rasters) {
      return null;
    }
    return (
      continuousFieldIndex.rasters.find(
        (raster) =>
          raster.component === componentId && raster.metric === metricId
      ) || null
    );
  }

  function rasterForComponent(componentId) {
    if (!continuousFieldIndex || !continuousFieldIndex.rasters) {
      return null;
    }
    return (
      continuousFieldIndex.rasters.find(
        (raster) => raster.component === componentId
      ) || null
    );
  }

  function metricsAvailableForComponent(componentId) {
    if (!continuousFieldIndex || !continuousFieldIndex.rasters) {
      return new Set();
    }
    return new Set(
      continuousFieldIndex.rasters
        .filter((raster) => raster.component === componentId)
        .map((raster) => raster.metric)
    );
  }

  function populateContinuousFieldSelector() {
    const componentSelect = document.querySelector(
      '#civvec-continuous-component-select'
    );
    if (!componentSelect || !continuousFieldIndex || !continuousFieldIndex.rasters) {
      return;
    }
    const componentsGroupedByReadMode = new Map();
    const seenComponents = new Set();
    for (const raster of continuousFieldIndex.rasters) {
      if (seenComponents.has(raster.component)) {
        continue;
      }
      seenComponents.add(raster.component);
      const readMode = raster.read_mode || 'raw';
      if (!componentsGroupedByReadMode.has(readMode)) {
        componentsGroupedByReadMode.set(readMode, []);
      }
      componentsGroupedByReadMode.get(readMode).push(raster.component);
    }

    const optgroupMarkup = READ_MODE_GROUP_ORDER.map((readMode) => {
      const componentIds = componentsGroupedByReadMode.get(readMode);
      if (!componentIds || componentIds.length === 0) {
        return '';
      }
      const groupLabel = READ_MODE_GROUP_LABEL[readMode] || readMode;
      const options = componentIds
        .map((component) => {
          const label = componentLabels[component] || component.replace(/_/g, ' ');
          return `<option value="${component}" title="${escapeHtml(label)}">${escapeHtml(label)}</option>`;
        })
        .join('');
      return `<optgroup label="${escapeHtml(groupLabel)}">${options}</optgroup>`;
    }).join('');

    componentSelect.innerHTML = optgroupMarkup;
    componentSelect.value = currentContinuousField.component;
  }

  function updateContinuousMetricSelector() {
    const metricSelect = document.querySelector(
      'select[name="continuous-metric"]'
    );
    if (!metricSelect) return;
    const available = metricsAvailableForComponent(currentContinuousField.component);
    for (const option of metricSelect.options) {
      const supported = available.has(option.value);
      option.disabled = !supported;
      option.title = supported
        ? metricLabels[option.value] || option.value
        : 'Cette vue n’est pas disponible pour les indicateurs synthétiques (déjà scalaires agrégés).';
    }
    // If the current metric isn't supported for this component, fall back to mean.
    if (!available.has(currentContinuousField.metric)) {
      currentContinuousField.metric = available.has('mean')
        ? 'mean'
        : Array.from(available)[0] || 'mean';
      metricSelect.value = currentContinuousField.metric;
    }
  }

  function preloadPartnerRaster(componentId) {
    if (!componentId) return;
    const raster = rasterForComponent(componentId);
    if (!raster) return;
    const rasterUrl = `../assets/data/continuous_field/${raster.filename}`;
    if (preloadedRasterImages.has(rasterUrl)) return;
    const image = new Image();
    image.src = rasterUrl;
    preloadedRasterImages.set(rasterUrl, image);
  }

  function quadrantTableMarkup() {
    // Trois schémas de nommage superposés par quadrant (identité × tension).
    // Évocateur (gros), neutre (italique), description math (petit).
    const cellStyle =
      'border:1px solid #d0d4d9; padding:0.5em 0.6em; vertical-align:top; ' +
      'font-size:0.85em; line-height:1.35;';
    const headerStyle =
      'background:#eef2f6; font-weight:600; text-align:center; padding:0.35em 0.5em; ' +
      'font-size:0.85em;';
    const corner = `<th style="${headerStyle}; background:transparent; border:0;"></th>`;
    return `
<table style="border-collapse:collapse; margin:0.45em 0 0 0; width:100%; max-width:520px;">
  <tr>
    ${corner}
    <th style="${headerStyle}">Tension faible</th>
    <th style="${headerStyle}">Tension forte</th>
  </tr>
  <tr>
    <th style="${headerStyle}; text-align:right;">Identité<br/>forte</th>
    <td style="${cellStyle}; background:#eaf4ea;">
      <strong>Cœur stable</strong><br/>
      <em>Noyau</em><br/>
      <small>identité ↑, tension ↓</small>
    </td>
    <td style="${cellStyle}; background:#fdebe1;">
      <strong>Fracture entre cœurs</strong><br/>
      <em>Faille</em><br/>
      <small>identité ↑, tension ↑</small>
    </td>
  </tr>
  <tr>
    <th style="${headerStyle}; text-align:right;">Identité<br/>faible</th>
    <td style="${cellStyle}; background:#f3f0e6;">
      <strong>Plaine multiculturelle</strong><br/>
      <em>Zone diffuse</em><br/>
      <small>identité ↓, tension ↓</small>
    </td>
    <td style="${cellStyle}; background:#fbe6f0;">
      <strong>Chaos transitionnel</strong><br/>
      <em>Turbulence</em><br/>
      <small>identité ↓, tension ↑</small>
    </td>
  </tr>
</table>`;
  }

  function updateContinuousReadModeBanner() {
    const bannerElement = document.querySelector(
      '#civvec-continuous-mode-banner'
    );
    if (!bannerElement) return;
    const raster = rasterByComponentAndMetric(
      currentContinuousField.component,
      currentContinuousField.metric
    ) || rasterForComponent(currentContinuousField.component);
    if (!raster) {
      bannerElement.style.display = 'none';
      bannerElement.innerHTML = '';
      return;
    }
    const readMode = raster.read_mode || 'raw';
    if (readMode === 'paired') {
      const partnerComponent = raster.pair_with;
      const partnerLabel = partnerComponent
        ? componentLabels[partnerComponent] || partnerComponent
        : null;
      const swapButton = partnerComponent
        ? `<button type="button" data-action="swap-to-partner" data-target-component="${escapeHtml(partnerComponent)}" style="margin-top:0.4em; padding:0.3em 0.7em; font-size:0.85em; border:1px solid #6c8caf; background:#eaf2fa; color:#1a3a5c; border-radius:4px; cursor:pointer;">↔ Basculer vers : ${escapeHtml(partnerLabel)}</button>`
        : '';
      bannerElement.innerHTML = `
<div style="border-left:4px solid #6c8caf; background:#f4f8fc; padding:0.6em 0.85em; font-size:0.9em; border-radius:0 4px 4px 0;">
  <strong>Indicateur synthétique couplé.</strong>
  Ces deux indicateurs (force d’identité &amp; tension culturelle) ne se
  comprennent qu’en regardant les deux cartes ensemble. La grille
  ci-dessous donne la lecture conjointe :
  ${quadrantTableMarkup()}
  ${swapButton}
</div>`;
      bannerElement.style.display = 'block';
      if (partnerComponent) {
        preloadPartnerRaster(partnerComponent);
      }
      return;
    }
    if (readMode === 'standalone') {
      bannerElement.innerHTML = `
<div style="border-left:4px solid #2e7d32; background:#eaf4ea; padding:0.6em 0.85em; font-size:0.9em; border-radius:0 4px 4px 0;">
  <strong>Indicateur synthétique autonome.</strong>
  Cet indicateur se lit seul : il combine déjà position, identité et
  proximité aux frontières civilisationnelles en un seul scalaire.
  <ul style="margin:0.4em 0 0 1.2em; padding:0;">
    <li><strong>Élevé</strong> = cœur civilisationnel net et profond (la civilisation la plus proche est nettement plus proche que la deuxième).</li>
    <li><strong>Proche de 0</strong> = lieu équidistant de deux civilisations = <em>fault line</em>.</li>
  </ul>
</div>`;
      bannerElement.style.display = 'block';
      return;
    }
    // Composante brute — pas de bandeau interprétatif.
    bannerElement.style.display = 'none';
    bannerElement.innerHTML = '';
  }

  async function loadContinuousFieldIndex() {
    if (continuousFieldIndex !== null) {
      return continuousFieldIndex;
    }
    try {
      continuousFieldIndex = await fetchJson(
        '../assets/data/continuous_field/index.json'
      );
    } catch (error) {
      console.warn('[civvec/map] continuous field index unavailable', error);
      continuousFieldIndex = { rasters: [], bbox: null };
    }
    return continuousFieldIndex;
  }

  function applyDisplayMode(map, legendContainer, mode) {
    const allowedModes = ['macro', 'sub', 'provenance', 'continuous', 'plates'];
    currentDisplayMode = allowedModes.includes(mode) ? mode : 'macro';
    const propertyKeyByMode = {
      macro: 'fill_color_macro',
      sub: 'fill_color_sub',
      provenance: 'fill_color_provenance'
    };

    const continuousLayerExists = map.getLayer('continuous-field-layer');
    if (currentDisplayMode === 'continuous') {
      if (map.getLayer('states-fill')) {
        map.setPaintProperty('states-fill', 'fill-opacity', 0.0);
      }
      if (continuousLayerExists) {
        map.setLayoutProperty('continuous-field-layer', 'visibility', 'visible');
      }
      applyContinuousFieldRaster(map);
      refreshPlatesLayerVisibility(map);
    } else if (currentDisplayMode === 'plates') {
      if (map.getLayer('states-fill')) {
        map.setPaintProperty('states-fill', 'fill-opacity', 0.0);
      }
      if (continuousLayerExists) {
        map.setLayoutProperty('continuous-field-layer', 'visibility', 'none');
      }
      applyPlatesMode(map).catch((error) =>
        console.error('[civvec/map] applyPlatesMode a échoué', error)
      );
    } else {
      const propertyKey = propertyKeyByMode[currentDisplayMode];
      if (map.getLayer('states-fill')) {
        map.setPaintProperty('states-fill', 'fill-color', [
          'coalesce',
          ['get', propertyKey],
          fallbackColor
        ]);
        map.setPaintProperty('states-fill', 'fill-opacity', [
          'coalesce',
          ['get', 'fill_opacity'],
          0.78
        ]);
      }
      if (continuousLayerExists) {
        map.setLayoutProperty('continuous-field-layer', 'visibility', 'none');
      }
      refreshPlatesLayerVisibility(map);
    }

    const continuousSelectorContainer = document.querySelector(
      '#civvec-map-continuous-selector'
    );
    if (continuousSelectorContainer) {
      continuousSelectorContainer.style.display =
        currentDisplayMode === 'continuous' ? 'flex' : 'none';
    }
    const platesTogglesContainer = document.querySelector('#civvec-map-plates-toggles');
    if (platesTogglesContainer) {
      platesTogglesContainer.style.display =
        currentDisplayMode === 'plates' ? 'flex' : 'none';
    }
    const bannerElement = document.querySelector(
      '#civvec-continuous-mode-banner'
    );
    if (bannerElement) {
      bannerElement.style.display =
        currentDisplayMode === 'continuous' ? bannerElement.style.display || 'block' : 'none';
    }
    if (currentDisplayMode === 'continuous') {
      updateContinuousMetricSelector();
      updateContinuousReadModeBanner();
    }

    if (legendContainer) {
      buildLegend(legendContainer, currentDisplayMode);
    }
  }

  function applyContinuousFieldRaster(map) {
    const sourceId = 'continuous-field-source';
    const layerId = 'continuous-field-layer';
    const rasterUrl = `../assets/data/continuous_field/${currentContinuousField.component}_${currentContinuousField.metric}.png`;

    // MapLibre image sources are projected to Web Mercator; latitudes of
    // ±90° map to ±Infinity. Clamp the corner latitudes to the standard
    // Web Mercator bounds (≈ ±85.0511°) so MapLibre can place the raster.
    const WEB_MERCATOR_LATITUDE_BOUND_DEG = 85.0511;
    const bboxRaw =
      (continuousFieldIndex && continuousFieldIndex.bbox) || {
        longitude_min_deg: -180,
        longitude_max_deg: 180,
        latitude_min_deg: -90,
        latitude_max_deg: 90
      };
    const clampLatitude = (latitude) =>
      Math.max(
        -WEB_MERCATOR_LATITUDE_BOUND_DEG,
        Math.min(WEB_MERCATOR_LATITUDE_BOUND_DEG, latitude)
      );
    const bbox = {
      longitude_min_deg: bboxRaw.longitude_min_deg,
      longitude_max_deg: bboxRaw.longitude_max_deg,
      latitude_min_deg: clampLatitude(bboxRaw.latitude_min_deg),
      latitude_max_deg: clampLatitude(bboxRaw.latitude_max_deg)
    };
    const coordinates = [
      [bbox.longitude_min_deg, bbox.latitude_max_deg],
      [bbox.longitude_max_deg, bbox.latitude_max_deg],
      [bbox.longitude_max_deg, bbox.latitude_min_deg],
      [bbox.longitude_min_deg, bbox.latitude_min_deg]
    ];

    if (map.getSource(sourceId)) {
      try {
        map.getSource(sourceId).updateImage({ url: rasterUrl, coordinates });
      } catch (error) {
        console.warn('[civvec/map] updateImage failed, recreating source', error);
        map.removeLayer(layerId);
        map.removeSource(sourceId);
      }
    }

    if (!map.getSource(sourceId)) {
      map.addSource(sourceId, {
        type: 'image',
        url: rasterUrl,
        coordinates
      });
      map.addLayer(
        {
          id: layerId,
          source: sourceId,
          type: 'raster',
          paint: {
            'raster-opacity': 0.85
          }
        },
        'states-outline'
      );
    } else if (!map.getLayer(layerId)) {
      map.addLayer(
        {
          id: layerId,
          source: sourceId,
          type: 'raster',
          paint: {
            'raster-opacity': 0.85
          }
        },
        'states-outline'
      );
    }
  }

  function wireModeToggle(map, legendContainer) {
    const modeContainer = document.querySelector(modeContainerSelector);
    if (modeContainer) {
      modeContainer.addEventListener('change', (changeEvent) => {
        const target = changeEvent.target;
        if (!target || target.name !== 'civvec-map-mode') {
          return;
        }
        applyDisplayMode(map, legendContainer, target.value);
      });
    }

    const continuousSelector = document.querySelector(
      '#civvec-map-continuous-selector'
    );
    if (continuousSelector) {
      continuousSelector.addEventListener('change', (changeEvent) => {
        const target = changeEvent.target;
        if (!target) return;
        if (target.name === 'continuous-component') {
          currentContinuousField.component = target.value;
          updateContinuousMetricSelector();
        } else if (target.name === 'continuous-metric') {
          currentContinuousField.metric = target.value;
        } else {
          return;
        }
        if (currentDisplayMode === 'continuous') {
          applyContinuousFieldRaster(map);
          updateContinuousReadModeBanner();
          if (legendContainer) {
            buildLegend(legendContainer, currentDisplayMode);
          }
        }
      });
    }

    const platesTogglesContainer = document.querySelector('#civvec-map-plates-toggles');
    if (platesTogglesContainer) {
      platesTogglesContainer.addEventListener('change', (changeEvent) => {
        const target = changeEvent.target;
        if (!target || !target.dataset || !target.dataset.platesLayer) return;
        const layerKey = target.dataset.platesLayer;
        if (!(layerKey in platesLayerToggleState)) return;
        platesLayerToggleState[layerKey] = !!target.checked;
        if (currentDisplayMode === 'plates') {
          refreshPlatesLayerVisibility(map);
        }
      });
    }

    // Bouton « Basculer vers le partenaire » (présent dans le bandeau lecture couplée).
    const bannerElement = document.querySelector(
      '#civvec-continuous-mode-banner'
    );
    if (bannerElement) {
      bannerElement.addEventListener('click', (clickEvent) => {
        const target = clickEvent.target;
        if (!target || target.getAttribute('data-action') !== 'swap-to-partner') {
          return;
        }
        const partnerComponent = target.getAttribute('data-target-component');
        if (!partnerComponent) return;
        currentContinuousField.component = partnerComponent;
        const componentSelectElement = document.querySelector(
          '#civvec-continuous-component-select'
        );
        if (componentSelectElement) {
          componentSelectElement.value = partnerComponent;
        }
        updateContinuousMetricSelector();
        if (currentDisplayMode === 'continuous') {
          applyContinuousFieldRaster(map);
          updateContinuousReadModeBanner();
          if (legendContainer) {
            buildLegend(legendContainer, currentDisplayMode);
          }
        }
      });
    }
  }

  async function bootstrapMap() {
    const [statesGeojson, stateCoordinatesPayload] = await Promise.all([
      fetchJson('../assets/data/global_state_baseline.geojson'),
      fetchJson('../assets/data/state_coordinates.json')
    ]);

    await loadContinuousFieldIndex();

    const stateCoordinatesByIso3 = indexStateCoordinatesByIso3(stateCoordinatesPayload);
    const decoratedGeojson = decorateFeaturesWithMembership(
      statesGeojson,
      stateCoordinatesByIso3
    );

    const legendContainer = document.querySelector(legendContainerSelector);
    if (legendContainer) {
      buildLegend(legendContainer, currentDisplayMode);
    }

    populateContinuousFieldSelector();
    injectPlatesModeControls();

    const map = new maplibregl.Map({
      container: 'civvec-map',
      style: {
        version: 8,
        sources: {},
        layers: [
          {
            id: 'background',
            type: 'background',
            paint: { 'background-color': '#f5f5f5' }
          }
        ]
      },
      center: [10, 15],
      zoom: 0.4,
      maxZoom: 4,
      minZoom: 0.2
    });

    let hoveredFeatureId = null;

    map.on('load', () => {
      map.addSource('states', {
        type: 'geojson',
        data: decoratedGeojson,
        generateId: true
      });
      map.addLayer({
        id: 'states-fill',
        type: 'fill',
        source: 'states',
        paint: {
          'fill-color': ['coalesce', ['get', 'fill_color_macro'], fallbackColor],
          'fill-opacity': ['coalesce', ['get', 'fill_opacity'], 0.78]
        }
      });
      map.addLayer({
        id: 'states-outline',
        type: 'line',
        source: 'states',
        paint: { 'line-color': '#333', 'line-width': 0.5 }
      });
      map.addLayer({
        id: 'states-outline-hover',
        type: 'line',
        source: 'states',
        paint: {
          'line-color': '#111',
          'line-width': [
            'case',
            ['boolean', ['feature-state', 'hover'], false],
            1.6,
            0
          ]
        }
      });
      applyDisplayMode(map, legendContainer, currentDisplayMode);
      wireModeToggle(map, legendContainer);
    });

    const hoverTooltip = new maplibregl.Popup({
      closeButton: false,
      closeOnClick: false,
      offset: 10,
      className: 'civvec-map-tooltip'
    });

    map.on('click', 'states-fill', (clickEvent) => {
      const feature = clickEvent.features && clickEvent.features[0];
      if (!feature) return;
      const properties = feature.properties || {};
      const iso3 = properties.iso3 || '?';
      const nameFr = properties.name_fr || properties.NAME_FR || iso3;
      const curated = properties.curated_civilization;
      const curatedRole = properties.curated_role;
      const affinityCiv = properties.affinity_top_civilization;
      const affinityWeight = properties.affinity_top_weight;
      const subLabel = properties.sub_cluster_label;
      const origin = properties.effective_origin;
      const effective = properties.effective_civilization || 'inconnue';
      const originBadge =
        origin === 'curated'
          ? '<small>(curatée)</small>'
          : origin === 'fallback'
            ? '<small>(centroïde de repli)</small>'
            : origin === 'affinity'
              ? '<small>(par affinité argmax)</small>'
              : '<small>(aucune donnée)</small>';
      const weightDisplay =
        typeof affinityWeight === 'number' || (typeof affinityWeight === 'string' && affinityWeight !== '')
          ? Number(affinityWeight).toFixed(3)
          : '—';
      const vizProvenance = properties.x_viz_provenance || 'unresolved';
      const scoreProvenance = properties.x_score_provenance || 'unresolved';
      const fallbackCivilization = properties.fallback_civilization_id;
      const provenanceWarning =
        vizProvenance !== 'observed' || !['observed', 'observed_with_dim_imputation'].includes(scoreProvenance)
          ? '<div style="color:#b35900; font-size:0.85em; margin-top:0.3em;">⚠️ Au moins une coordonnée est <strong>imputée ou prior</strong> — n\'utilise pas comme mesure directe.</div>'
          : '';
      const lines = [
        `<strong>${escapeHtml(nameFr)}</strong> <code>${escapeHtml(iso3)}</code> ${originBadge}`,
        `Civilisation : <code>${escapeHtml(effective)}</code>`,
        `Sous-ensemble : ${subLabel ? `<code>${escapeHtml(subLabel)}</code>` : '<em>—</em>'}`,
        `Curatée : ${curated ? `<code>${escapeHtml(curated)}</code> (${escapeHtml(curatedRole || '?')})` : '<em>aucune</em>'}`,
        `Argmax affinité : ${affinityCiv ? `<code>${escapeHtml(affinityCiv)}</code> (${weightDisplay})` : '<em>—</em>'}`,
        `Provenance <code>x_viz</code> : <code>${escapeHtml(vizProvenance)}</code>`,
        `Provenance <code>x_score</code> : <code>${escapeHtml(scoreProvenance)}</code>` +
          (fallbackCivilization ? ` <small>(centroïde de repli : <code>${escapeHtml(fallbackCivilization)}</code>)</small>` : ''),
        '<em>Source géométrie : Natural Earth (domaine public)</em>',
        provenanceWarning
      ];
      new maplibregl.Popup()
        .setLngLat(clickEvent.lngLat)
        .setHTML(lines.join('<br/>'))
        .addTo(map);
    });

    map.on('mousemove', 'states-fill', (mouseEvent) => {
      if (!mouseEvent.features || mouseEvent.features.length === 0) {
        return;
      }
      const newFeature = mouseEvent.features[0];
      const newId = newFeature.id;
      if (hoveredFeatureId !== null && hoveredFeatureId !== newId) {
        map.setFeatureState({ source: 'states', id: hoveredFeatureId }, { hover: false });
      }
      hoveredFeatureId = newId;
      map.setFeatureState({ source: 'states', id: hoveredFeatureId }, { hover: true });
      map.getCanvas().style.cursor = 'pointer';
      const properties = newFeature.properties || {};
      const tooltipName = properties.name_fr || properties.NAME_FR || properties.iso3 || '?';
      const tooltipIso = properties.iso3 || '';
      hoverTooltip
        .setLngLat(mouseEvent.lngLat)
        .setHTML(
          `<strong>${escapeHtml(tooltipName)}</strong>${tooltipIso ? ` <code>${escapeHtml(tooltipIso)}</code>` : ''}`
        )
        .addTo(map);
    });
    map.on('mouseleave', 'states-fill', () => {
      if (hoveredFeatureId !== null) {
        map.setFeatureState({ source: 'states', id: hoveredFeatureId }, { hover: false });
      }
      hoveredFeatureId = null;
      map.getCanvas().style.cursor = '';
      hoverTooltip.remove();
    });
  }

  bootstrapMap().catch((error) => {
    console.error('[civvec/map] échec d\'initialisation', error);
    const mapContainer = document.querySelector(mapContainerSelector);
    if (mapContainer) {
      mapContainer.innerHTML =
        '<p style="padding: 1rem;">Carte indisponible — voir le téléchargement direct du GeoJSON ci-dessous.</p>';
    }
  });
})();
