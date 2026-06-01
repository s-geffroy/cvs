/*
 * civvec — Tenseurs de tension (Phase 2)
 *
 * Plotly — barres anisotropie A(s) triées + heatmap interactif 6×6 du
 * tenseur T(s) avec sélecteur d'État.
 */
(function initCivvecTensors() {
  const anisotropyContainerSelector = '#civvec-tensions-anisotropy';
  const heatmapContainerSelector = '#civvec-tensions-heatmap';
  if (!document.querySelector(anisotropyContainerSelector) && !document.querySelector(heatmapContainerSelector)) {
    return;
  }
  if (typeof Plotly === 'undefined') {
    console.warn('[civvec/tensors] Plotly.js non chargé — abandon.');
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

  function renderAnisotropyBars(tensorsPayload) {
    const tensorEntries = [...tensorsPayload.tensions].sort(
      (left, right) => right.anisotropy - left.anisotropy
    );
    const anisotropyTrace = {
      x: tensorEntries.map((entry) => entry.iso3),
      y: tensorEntries.map((entry) => entry.anisotropy),
      type: 'bar',
      marker: { color: '#d62728' }
    };
    const layout = {
      title: 'Anisotropie A(s) = (λ₁ − λ₆) / λ₁ — États triés',
      xaxis: { title: 'ISO3', tickangle: -60 },
      yaxis: { title: 'A(s) ∈ [0, 1]', range: [0, 1] },
      margin: { t: 60, l: 60, r: 30, b: 100 }
    };
    Plotly.newPlot('civvec-tensions-anisotropy', [anisotropyTrace], layout, {
      responsive: true,
      displaylogo: false
    });
  }

  function renderHeatmap(tensorEntry) {
    const heatmapTrace = {
      z: tensorEntry.T,
      x: hofstedeDimensionLabels,
      y: hofstedeDimensionLabels,
      type: 'heatmap',
      colorscale: 'RdBu',
      reversescale: true,
      colorbar: { title: 'T_ij' }
    };
    const layout = {
      title: `T(${tensorEntry.iso3}) — tenseur 6×6`,
      xaxis: { side: 'top' },
      yaxis: { autorange: 'reversed' },
      margin: { t: 60, l: 60, r: 30, b: 30 }
    };
    Plotly.newPlot('civvec-tensions-heatmap', [heatmapTrace], layout, {
      responsive: true,
      displaylogo: false
    });
  }

  function injectStateSelectorAbove(heatmapContainer, tensorEntries, defaultIso3) {
    const selectorWrapper = document.createElement('div');
    selectorWrapper.style.marginBottom = '0.5rem';
    selectorWrapper.innerHTML =
      '<label for="civvec-tensions-state-selector" style="margin-right:0.5rem;">État :</label>' +
      `<select id="civvec-tensions-state-selector">${tensorEntries
        .map(
          (entry) =>
            `<option value="${entry.iso3}"${entry.iso3 === defaultIso3 ? ' selected' : ''}>${entry.iso3}</option>`
        )
        .join('')}</select>`;
    heatmapContainer.parentNode.insertBefore(selectorWrapper, heatmapContainer);
    const stateSelectorElement = document.getElementById('civvec-tensions-state-selector');
    stateSelectorElement.addEventListener('change', (changeEvent) => {
      const selectedIso3 = changeEvent.target.value;
      const matched = tensorEntries.find((entry) => entry.iso3 === selectedIso3);
      if (matched) {
        renderHeatmap(matched);
      }
    });
  }

  async function bootstrapTensors() {
    const tensorsPayload = await fetchJson('../assets/data/state_tensors.json');
    const tensorEntries = tensorsPayload.tensions;

    if (document.querySelector(anisotropyContainerSelector)) {
      renderAnisotropyBars(tensorsPayload);
    }

    if (document.querySelector(heatmapContainerSelector) && tensorEntries.length > 0) {
      const heatmapContainer = document.querySelector(heatmapContainerSelector);
      const defaultIso3 = tensorEntries.find((entry) => entry.iso3 === 'FRA')
        ? 'FRA'
        : tensorEntries[0].iso3;
      injectStateSelectorAbove(heatmapContainer, tensorEntries, defaultIso3);
      const initialEntry = tensorEntries.find((entry) => entry.iso3 === defaultIso3);
      renderHeatmap(initialEntry);
    }
  }

  bootstrapTensors().catch((error) => {
    console.error('[civvec/tensors] échec d\'initialisation', error);
  });
})();
