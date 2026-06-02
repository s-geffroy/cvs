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
        continue;
      }
      const argmax = dominantCivilizationByAffinity(stateEntry.affinity_vector);
      const curatedCivilization = stateEntry.curated_civilization || null;
      const effectiveCivilization = curatedCivilization || argmax.civilizationId;
      const effectiveOrigin = curatedCivilization ? 'curated' : 'affinity';
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

  function applyDisplayMode(map, legendContainer, mode) {
    currentDisplayMode = mode === 'sub' ? 'sub' : 'macro';
    const propertyKey = currentDisplayMode === 'sub' ? 'fill_color_sub' : 'fill_color_macro';
    if (map.getLayer('states-fill')) {
      map.setPaintProperty('states-fill', 'fill-color', [
        'coalesce',
        ['get', propertyKey],
        fallbackColor
      ]);
    }
    if (legendContainer) {
      buildLegend(legendContainer, currentDisplayMode);
    }
  }

  function wireModeToggle(map, legendContainer) {
    const modeContainer = document.querySelector(modeContainerSelector);
    if (!modeContainer) {
      return;
    }
    modeContainer.addEventListener('change', (changeEvent) => {
      const target = changeEvent.target;
      if (!target || target.name !== 'civvec-map-mode') {
        return;
      }
      applyDisplayMode(map, legendContainer, target.value);
    });
  }

  async function bootstrapMap() {
    const [statesGeojson, stateCoordinatesPayload] = await Promise.all([
      fetchJson('../assets/data/global_state_baseline.geojson'),
      fetchJson('../assets/data/state_coordinates.json')
    ]);

    const stateCoordinatesByIso3 = indexStateCoordinatesByIso3(stateCoordinatesPayload);
    const decoratedGeojson = decorateFeaturesWithMembership(
      statesGeojson,
      stateCoordinatesByIso3
    );

    const legendContainer = document.querySelector(legendContainerSelector);
    if (legendContainer) {
      buildLegend(legendContainer, currentDisplayMode);
    }

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
      center: [10, 20],
      zoom: 1.2,
      maxZoom: 4,
      minZoom: 1.0
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
          'fill-opacity': 0.78
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
          : origin === 'affinity'
            ? '<small>(par affinité argmax)</small>'
            : '<small>(aucune donnée)</small>';
      const weightDisplay =
        typeof affinityWeight === 'number' || (typeof affinityWeight === 'string' && affinityWeight !== '')
          ? Number(affinityWeight).toFixed(3)
          : '—';
      const lines = [
        `<strong>${escapeHtml(nameFr)}</strong> <code>${escapeHtml(iso3)}</code> ${originBadge}`,
        `Civilisation : <code>${escapeHtml(effective)}</code>`,
        `Sous-ensemble : ${subLabel ? `<code>${escapeHtml(subLabel)}</code>` : '<em>—</em>'}`,
        `Curatée : ${curated ? `<code>${escapeHtml(curated)}</code> (${escapeHtml(curatedRole || '?')})` : '<em>aucune</em>'}`,
        `Argmax affinité : ${affinityCiv ? `<code>${escapeHtml(affinityCiv)}</code> (${weightDisplay})` : '<em>—</em>'}`,
        '<em>Source géométrie : Natural Earth (domaine public)</em>'
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
