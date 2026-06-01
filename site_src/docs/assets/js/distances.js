/*
 * civvec — Algèbre des distances (Phase 2)
 *
 * Plotly — heatmap de la matrice d_hyb + détail toutes-distances entre deux États.
 */
(function initCivvecDistances() {
  const heatmapContainerSelector = '#civvec-distances-heatmap';
  const pairContainerSelector = '#civvec-distances-pair';
  if (!document.querySelector(heatmapContainerSelector) && !document.querySelector(pairContainerSelector)) {
    return;
  }
  if (typeof Plotly === 'undefined') {
    console.warn('[civvec/distances] Plotly.js non chargé — abandon.');
    return;
  }

  async function fetchJson(relativeUrl) {
    const response = await fetch(relativeUrl);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status} pour ${relativeUrl}`);
    }
    return response.json();
  }

  function renderDistanceHeatmap(distancePayload) {
    const iso3List = distancePayload.iso3_order;
    const hybridMatrix = distancePayload.matrices.d_hybrid;
    const heatmapTrace = {
      z: hybridMatrix,
      x: iso3List,
      y: iso3List,
      type: 'heatmap',
      colorscale: 'Viridis',
      colorbar: { title: 'd_hyb' },
      hovertemplate: '<b>%{x}</b> ↔ <b>%{y}</b><br>d_hyb=%{z:.3f}<extra></extra>'
    };
    const layout = {
      title: 'Distance hybride d_hyb (α=0.4 d_score^M + β=0.4 d_w^W + γ=0.2 d_T)',
      xaxis: { tickangle: -75 },
      yaxis: { autorange: 'reversed' },
      margin: { t: 60, l: 80, r: 30, b: 100 }
    };
    Plotly.newPlot('civvec-distances-heatmap', [heatmapTrace], layout, {
      responsive: true,
      displaylogo: false
    });
  }

  function renderPairDetail(distancePayload, leftIso3, rightIso3) {
    const iso3List = distancePayload.iso3_order;
    const leftIndex = iso3List.indexOf(leftIso3);
    const rightIndex = iso3List.indexOf(rightIso3);
    const pairContainer = document.querySelector(pairContainerSelector);
    if (leftIndex < 0 || rightIndex < 0) {
      pairContainer.innerHTML = '<em>Sélection invalide.</em>';
      return;
    }
    const metricsRows = Object.entries(distancePayload.matrices)
      .map(([metricKey, matrix]) => {
        const value = matrix[leftIndex][rightIndex];
        return `<tr><td><code>${metricKey}</code></td><td>${Number(value).toFixed(4)}</td></tr>`;
      })
      .join('');
    pairContainer.innerHTML =
      `<table><thead><tr><th>Métrique</th><th>${leftIso3} ↔ ${rightIso3}</th></tr></thead>` +
      `<tbody>${metricsRows}</tbody></table>`;
  }

  function injectPairSelectors(distancePayload) {
    const iso3List = distancePayload.iso3_order;
    const pairContainer = document.querySelector(pairContainerSelector);
    if (!pairContainer) {
      return;
    }
    const selectorWrapper = document.createElement('div');
    selectorWrapper.style.marginBottom = '0.5rem';
    selectorWrapper.innerHTML =
      '<label>État A : <select id="civvec-distances-state-a">' +
      iso3List.map((iso3) => `<option value="${iso3}">${iso3}</option>`).join('') +
      '</select></label> &nbsp; ' +
      '<label>État B : <select id="civvec-distances-state-b">' +
      iso3List.map((iso3) => `<option value="${iso3}">${iso3}</option>`).join('') +
      '</select></label>';
    pairContainer.parentNode.insertBefore(selectorWrapper, pairContainer);

    const stateAElement = document.getElementById('civvec-distances-state-a');
    const stateBElement = document.getElementById('civvec-distances-state-b');
    const defaultLeftIso3 = iso3List.includes('FRA') ? 'FRA' : iso3List[0];
    const defaultRightIso3 = iso3List.includes('JPN') ? 'JPN' : iso3List[Math.min(1, iso3List.length - 1)];
    stateAElement.value = defaultLeftIso3;
    stateBElement.value = defaultRightIso3;

    const onChange = () => {
      renderPairDetail(distancePayload, stateAElement.value, stateBElement.value);
    };
    stateAElement.addEventListener('change', onChange);
    stateBElement.addEventListener('change', onChange);
    renderPairDetail(distancePayload, defaultLeftIso3, defaultRightIso3);
  }

  async function bootstrapDistances() {
    const distancePayload = await fetchJson('../assets/data/state_distance_matrix.json');
    if (document.querySelector(heatmapContainerSelector)) {
      renderDistanceHeatmap(distancePayload);
    }
    if (document.querySelector(pairContainerSelector)) {
      injectPairSelectors(distancePayload);
    }
  }

  bootstrapDistances().catch((error) => {
    console.error('[civvec/distances] échec d\'initialisation', error);
  });
})();
