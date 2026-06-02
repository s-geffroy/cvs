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

  function labelForIso3(iso3, iso3ToNameFr) {
    const nameFr = iso3ToNameFr[iso3];
    return nameFr ? `${nameFr} (${iso3})` : iso3;
  }

  function renderDistanceHeatmap(distancePayload, iso3ToNameFr) {
    const iso3List = distancePayload.iso3_order;
    const hybridMatrix = distancePayload.matrices.d_hybrid;
    const labels = iso3List.map((iso3) => labelForIso3(iso3, iso3ToNameFr));
    const heatmapTrace = {
      z: hybridMatrix,
      x: labels,
      y: labels,
      type: 'heatmap',
      colorscale: 'Viridis',
      colorbar: { title: 'd_hyb' },
      hovertemplate: '<b>%{x}</b> ↔ <b>%{y}</b><br>d_hyb=%{z:.3f}<extra></extra>'
    };
    const layout = {
      title: 'Distance hybride d_hyb (α=0.4 d_score^M + β=0.4 d_w^W + γ=0.2 d_T)',
      xaxis: { tickangle: -75 },
      yaxis: { autorange: 'reversed' },
      margin: { t: 60, l: 160, r: 30, b: 160 }
    };
    Plotly.newPlot('civvec-distances-heatmap', [heatmapTrace], layout, {
      responsive: true,
      displaylogo: false
    });
  }

  function renderPairDetail(distancePayload, leftIso3, rightIso3, iso3ToNameFr) {
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
      `<table><thead><tr><th>Métrique</th><th>${labelForIso3(leftIso3, iso3ToNameFr)} ↔ ${labelForIso3(rightIso3, iso3ToNameFr)}</th></tr></thead>` +
      `<tbody>${metricsRows}</tbody></table>`;
  }

  function injectPairSelectors(distancePayload, iso3ToNameFr) {
    const iso3List = distancePayload.iso3_order;
    const pairContainer = document.querySelector(pairContainerSelector);
    if (!pairContainer) {
      return;
    }
    const optionsHtml = iso3List
      .map((iso3) => `<option value="${iso3}">${labelForIso3(iso3, iso3ToNameFr)}</option>`)
      .join('');
    const selectorWrapper = document.createElement('div');
    selectorWrapper.style.marginBottom = '0.5rem';
    selectorWrapper.innerHTML =
      `<label>État A : <select id="civvec-distances-state-a">${optionsHtml}</select></label> &nbsp; ` +
      `<label>État B : <select id="civvec-distances-state-b">${optionsHtml}</select></label>`;
    pairContainer.parentNode.insertBefore(selectorWrapper, pairContainer);

    const stateAElement = document.getElementById('civvec-distances-state-a');
    const stateBElement = document.getElementById('civvec-distances-state-b');
    const defaultLeftIso3 = iso3List.includes('FRA') ? 'FRA' : iso3List[0];
    const defaultRightIso3 = iso3List.includes('JPN') ? 'JPN' : iso3List[Math.min(1, iso3List.length - 1)];
    stateAElement.value = defaultLeftIso3;
    stateBElement.value = defaultRightIso3;

    const onChange = () => {
      renderPairDetail(distancePayload, stateAElement.value, stateBElement.value, iso3ToNameFr);
    };
    stateAElement.addEventListener('change', onChange);
    stateBElement.addEventListener('change', onChange);
    renderPairDetail(distancePayload, defaultLeftIso3, defaultRightIso3, iso3ToNameFr);
  }

  async function bootstrapDistances() {
    const distancePayload = await fetchJson('../assets/data/state_distance_matrix.json');
    const iso3ToNameFr = (distancePayload._meta && distancePayload._meta.iso3_to_name_fr) || {};
    if (document.querySelector(heatmapContainerSelector)) {
      renderDistanceHeatmap(distancePayload, iso3ToNameFr);
    }
    if (document.querySelector(pairContainerSelector)) {
      injectPairSelectors(distancePayload, iso3ToNameFr);
    }
  }

  bootstrapDistances().catch((error) => {
    console.error('[civvec/distances] échec d\'initialisation', error);
  });
})();
