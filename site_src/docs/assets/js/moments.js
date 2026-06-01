/*
 * civvec — Second moments civilisationnels M(s) (Phase 2 / v3.0)
 *
 * Plotly — barres anisotropie A(s) triées + heatmap interactif 6×6 du
 * second moment M(s) avec sélecteur d'État.
 */
(function initCivvecMoments() {
  const anisotropyContainerSelector = '#civvec-moments-anisotropy';
  const heatmapContainerSelector = '#civvec-moments-heatmap';
  if (
    !document.querySelector(anisotropyContainerSelector)
    && !document.querySelector(heatmapContainerSelector)
  ) {
    return;
  }
  if (typeof Plotly === 'undefined') {
    console.warn('[civvec/moments] Plotly.js non chargé — abandon.');
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

  function renderAnisotropyBars(momentsPayload) {
    const momentEntries = [...momentsPayload.moments].sort(
      (left, right) => right.anisotropy - left.anisotropy
    );
    const anisotropyTrace = {
      x: momentEntries.map((entry) => entry.iso3),
      y: momentEntries.map((entry) => entry.anisotropy),
      type: 'bar',
      marker: { color: '#d62728' }
    };
    const layout = {
      title: 'Anisotropie A(s) = (λ₁ − λ₆) / λ₁ — États triés',
      xaxis: { title: 'ISO3', tickangle: -60 },
      yaxis: { title: 'A(s) ∈ [0, 1]', range: [0, 1] },
      margin: { t: 60, l: 60, r: 30, b: 100 }
    };
    Plotly.newPlot('civvec-moments-anisotropy', [anisotropyTrace], layout, {
      responsive: true,
      displaylogo: false
    });
  }

  function renderHeatmap(momentEntry) {
    const heatmapTrace = {
      z: momentEntry.M,
      x: hofstedeDimensionLabels,
      y: hofstedeDimensionLabels,
      type: 'heatmap',
      colorscale: 'RdBu',
      reversescale: true,
      colorbar: { title: 'M_ij' }
    };
    const layout = {
      title: `M(${momentEntry.iso3}) — second moment 6×6`,
      xaxis: { side: 'top' },
      yaxis: { autorange: 'reversed' },
      margin: { t: 60, l: 60, r: 30, b: 30 }
    };
    Plotly.newPlot('civvec-moments-heatmap', [heatmapTrace], layout, {
      responsive: true,
      displaylogo: false
    });
  }

  function injectStateSelectorAbove(heatmapContainer, momentEntries, defaultIso3) {
    const selectorWrapper = document.createElement('div');
    selectorWrapper.style.marginBottom = '0.5rem';
    selectorWrapper.innerHTML =
      '<label for="civvec-moments-state-selector" style="margin-right:0.5rem;">État :</label>' +
      `<select id="civvec-moments-state-selector">${momentEntries
        .map(
          (entry) =>
            `<option value="${entry.iso3}"${entry.iso3 === defaultIso3 ? ' selected' : ''}>${entry.iso3}</option>`
        )
        .join('')}</select>`;
    heatmapContainer.parentNode.insertBefore(selectorWrapper, heatmapContainer);
    const stateSelectorElement = document.getElementById('civvec-moments-state-selector');
    stateSelectorElement.addEventListener('change', (changeEvent) => {
      const selectedIso3 = changeEvent.target.value;
      const matchedEntry = momentEntries.find((entry) => entry.iso3 === selectedIso3);
      if (matchedEntry) {
        renderHeatmap(matchedEntry);
      }
    });
  }

  async function bootstrapMoments() {
    const momentsPayload = await fetchJson('../assets/data/state_moments.json');
    const momentEntries = momentsPayload.moments;

    if (document.querySelector(anisotropyContainerSelector)) {
      renderAnisotropyBars(momentsPayload);
    }

    if (document.querySelector(heatmapContainerSelector) && momentEntries.length > 0) {
      const heatmapContainer = document.querySelector(heatmapContainerSelector);
      const defaultIso3 = momentEntries.find((entry) => entry.iso3 === 'FRA')
        ? 'FRA'
        : momentEntries[0].iso3;
      injectStateSelectorAbove(heatmapContainer, momentEntries, defaultIso3);
      const initialEntry = momentEntries.find((entry) => entry.iso3 === defaultIso3);
      renderHeatmap(initialEntry);
    }
  }

  bootstrapMoments().catch((error) => {
    console.error('[civvec/moments] échec d\'initialisation', error);
  });
})();
