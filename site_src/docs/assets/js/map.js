/*
 * civvec — Carte interactive (Phase 2)
 *
 * MapLibre GL JS — choropleth des États souverains coloriés par civilisation
 * dominante (argmax du vecteur d'affinité dans B_score). Aucun appel à un
 * fond de carte externe : seuls les polygones Natural Earth 110m sont rendus.
 */
(function initCivvecMap() {
  const mapContainerSelector = '#civvec-map';
  const legendContainerSelector = '#civvec-map-legend';
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

  function decorateFeaturesWithCivilization(geojsonCollection, stateCoordinatesByIso3) {
    for (const feature of geojsonCollection.features) {
      const iso3 = feature.properties.iso3;
      const stateEntry = stateCoordinatesByIso3[iso3];
      if (!stateEntry) {
        feature.properties.dominant_civilization = null;
        feature.properties.dominant_weight = null;
        feature.properties.fill_color = fallbackColor;
        continue;
      }
      const dominant = dominantCivilizationByAffinity(stateEntry.affinity_vector);
      feature.properties.dominant_civilization = dominant.civilizationId;
      feature.properties.dominant_weight = dominant.weight;
      feature.properties.fill_color =
        civilizationColorPalette[dominant.civilizationId] || fallbackColor;
    }
    return geojsonCollection;
  }

  function buildLegend(legendContainer) {
    legendContainer.innerHTML =
      '<strong>Légende — civilisation dominante par affinité (B_score)</strong><br/>' +
      Object.entries(civilizationColorPalette)
        .map(
          ([civilizationId, color]) =>
            `<span style="display:inline-block;width:0.9em;height:0.9em;background:${color};margin-right:0.3em;vertical-align:middle;"></span>${civilizationId}`
        )
        .join(' &nbsp; ');
  }

  async function bootstrapMap() {
    const [statesGeojson, stateCoordinatesPayload] = await Promise.all([
      fetchJson('../assets/data/global_state_baseline.geojson'),
      fetchJson('../assets/data/state_coordinates.json')
    ]);

    const stateCoordinatesByIso3 = indexStateCoordinatesByIso3(stateCoordinatesPayload);
    const decoratedGeojson = decorateFeaturesWithCivilization(
      statesGeojson,
      stateCoordinatesByIso3
    );

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

    map.on('load', () => {
      map.addSource('states', { type: 'geojson', data: decoratedGeojson });
      map.addLayer({
        id: 'states-fill',
        type: 'fill',
        source: 'states',
        paint: {
          'fill-color': ['coalesce', ['get', 'fill_color'], fallbackColor],
          'fill-opacity': 0.78
        }
      });
      map.addLayer({
        id: 'states-outline',
        type: 'line',
        source: 'states',
        paint: { 'line-color': '#333', 'line-width': 0.3 }
      });
    });

    map.on('click', 'states-fill', (clickEvent) => {
      const feature = clickEvent.features && clickEvent.features[0];
      if (!feature) return;
      const properties = feature.properties || {};
      const dominantCivilizationLabel = properties.dominant_civilization || 'inconnue';
      const dominantWeightLabel = properties.dominant_weight
        ? Number(properties.dominant_weight).toFixed(3)
        : '—';
      new maplibregl.Popup()
        .setLngLat(clickEvent.lngLat)
        .setHTML(
          `<strong>${properties.iso3 || '?'}</strong><br/>` +
            `Civilisation dominante : <code>${dominantCivilizationLabel}</code><br/>` +
            `Affinité : <code>${dominantWeightLabel}</code><br/>` +
            `<em>Source géométrie : Natural Earth 110m (domaine public)</em>`
        )
        .addTo(map);
    });

    map.on('mouseenter', 'states-fill', () => {
      map.getCanvas().style.cursor = 'pointer';
    });
    map.on('mouseleave', 'states-fill', () => {
      map.getCanvas().style.cursor = '';
    });
  }

  const legendContainer = document.querySelector(legendContainerSelector);
  if (legendContainer) {
    buildLegend(legendContainer);
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
