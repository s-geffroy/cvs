/*
 * civvec — Base vectorielle B_vec (Phase 2)
 *
 * Plotly.js — scatter B_viz (Inglehart-Welzel) avec les 11 centroïdes
 * civilisationnels et la nuée d'États ; radar B_score (Hofstede 6D) avec
 * sélecteur de civilisation.
 */
(function initCivvecBasisViz() {
  const scatterContainerSelector = '#civvec-basis-scatter';
  const radarContainerSelector = '#civvec-basis-radar';
  if (!document.querySelector(scatterContainerSelector) && !document.querySelector(radarContainerSelector)) {
    return;
  }
  if (typeof Plotly === 'undefined') {
    console.warn('[civvec/basis] Plotly.js non chargé — abandon.');
    return;
  }

  const hofstedeDimensionLabels = ['PDI', 'IDV', 'MAS', 'UAI', 'LTO', 'IVR'];

  async function fetchJson(relativeUrl) {
    const response = await fetch(relativeUrl);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status} pour ${relativeUrl}`);
    }
    return response.json();
  }

  function renderScatterBviz(centroidsPayload, stateCoordinatesPayload) {
    const centroidEntries = centroidsPayload.centroids;
    const stateEntries = stateCoordinatesPayload.states;

    const centroidsTrace = {
      x: centroidEntries.map((centroid) => centroid.mu_viz[0]),
      y: centroidEntries.map((centroid) => centroid.mu_viz[1]),
      text: centroidEntries.map((centroid) => centroid.civilization_id),
      mode: 'markers+text',
      type: 'scatter',
      name: 'Centroïdes civilisationnels (μ_viz)',
      marker: { size: 16, symbol: 'star', color: 'crimson' },
      textposition: 'top center',
      textfont: { size: 11 }
    };

    const eligibleStates = stateEntries.filter(
      (stateEntry) => Array.isArray(stateEntry.x_viz) && stateEntry.x_viz[0] !== null
    );
    const statesTrace = {
      x: eligibleStates.map((stateEntry) => stateEntry.x_viz[0]),
      y: eligibleStates.map((stateEntry) => stateEntry.x_viz[1]),
      text: eligibleStates.map((stateEntry) => stateEntry.iso3),
      mode: 'markers',
      type: 'scatter',
      name: 'États (x_viz)',
      marker: { size: 6, color: '#1f77b4', opacity: 0.65 },
      hovertemplate: '<b>%{text}</b><br>TS=%{x:.2f}<br>SE=%{y:.2f}<extra></extra>'
    };

    const layout = {
      title: 'B_viz — Cultural Map (Inglehart-Welzel)',
      xaxis: { title: 'Traditional ↔ Secular-Rational (TS)', zeroline: true },
      yaxis: { title: 'Survival ↔ Self-Expression (SE)', zeroline: true },
      legend: { orientation: 'h', y: -0.2 },
      margin: { t: 50, l: 60, r: 30, b: 60 }
    };

    Plotly.newPlot('civvec-basis-scatter', [statesTrace, centroidsTrace], layout, {
      responsive: true,
      displaylogo: false
    });
  }

  function renderRadarBscore(centroidsPayload) {
    const centroidEntries = centroidsPayload.centroids;

    const radarTraces = centroidEntries.map((centroid) => ({
      type: 'scatterpolar',
      r: [...centroid.mu_score, centroid.mu_score[0]],
      theta: [...hofstedeDimensionLabels, hofstedeDimensionLabels[0]],
      fill: 'toself',
      name: centroid.civilization_id
    }));

    const layout = {
      title: 'B_score — Hofstede 6D (centroïdes)',
      polar: { radialaxis: { visible: true, range: [0, 100] } },
      legend: { orientation: 'v' },
      margin: { t: 60, l: 30, r: 30, b: 30 }
    };

    Plotly.newPlot('civvec-basis-radar', radarTraces, layout, {
      responsive: true,
      displaylogo: false
    });
  }

  async function bootstrapBasisViz() {
    const [centroidsPayload, stateCoordinatesPayload] = await Promise.all([
      fetchJson('../assets/data/civilization_centroids.json'),
      fetchJson('../assets/data/state_coordinates.json')
    ]);

    if (document.querySelector(scatterContainerSelector)) {
      renderScatterBviz(centroidsPayload, stateCoordinatesPayload);
    }
    if (document.querySelector(radarContainerSelector)) {
      renderRadarBscore(centroidsPayload);
    }
  }

  bootstrapBasisViz().catch((error) => {
    console.error('[civvec/basis] échec d\'initialisation', error);
  });
})();
