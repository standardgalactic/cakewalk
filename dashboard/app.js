let candidates = [];
let selected = null;

const candidateList = document.getElementById('candidateList');
const editorForm = document.getElementById('editorForm');
const emptyEditor = document.getElementById('emptyEditor');
const refreshButton = document.getElementById('refreshButton');
const audioPreview = document.getElementById('audioPreview');
const videoPreview = document.getElementById('videoPreview');
const visualPreview = document.getElementById('visualPreview');
const metaPreview = document.getElementById('metaPreview');

const fields = {
  itemId: document.getElementById('itemId'),
  title: document.getElementById('title'),
  description: document.getElementById('description'),
  visualizer: document.getElementById('visualizer'),
  speed: document.getElementById('speed'),
  tone: document.getElementById('tone'),
  ready: document.getElementById('ready')
};

async function fetchJson(url, options) {
  const response = await fetch(url, options);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

function renderCandidateList() {
  candidateList.innerHTML = '';
  candidates.forEach(candidate => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = `candidate ${selected && selected.id === candidate.id ? 'active' : ''}`;
    const cfg = candidate.config || {};
    button.innerHTML = `
      <strong>${cfg.title || candidate.title}</strong>
      <small>${candidate.repo} · ${candidate.status}</small>
      <small>${candidate.mp3.split('/').pop()}</small>
    `;
    button.onclick = () => selectCandidate(candidate.id);
    candidateList.appendChild(button);
  });
}

function buildVisualizerUrl(candidate) {
  const mp3 = encodeURIComponent(`../${candidate.mp3}`);
  const vtt = encodeURIComponent(`../${candidate.vtt}`);
  return `../visualizer/lissajous.html?audio=${mp3}&vtt=${vtt}`;
}

function fillEditor(candidate) {
  const cfg = candidate.config || {
    id: candidate.id,
    title: candidate.title,
    description: '',
    visualizer: 'static',
    speed: 1,
    tone: 1,
    ready: false,
    mp3: candidate.mp3,
    vtt: candidate.vtt,
    pdf: candidate.pdf
  };

  fields.itemId.value = cfg.id;
  fields.title.value = cfg.title || '';
  fields.description.value = cfg.description || '';
  fields.visualizer.value = cfg.visualizer || 'static';
  fields.speed.value = cfg.speed ?? 1;
  fields.tone.value = cfg.tone ?? 1;
  fields.ready.value = String(Boolean(cfg.ready));

  audioPreview.src = `/media/${candidate.mp3.replace(/^.*cakewalk\//, '')}`;
  const renderedVideo = candidate.rendered_video || (candidate.config && candidate.config.rendered_video);
  videoPreview.src = renderedVideo ? `/media/${renderedVideo.replace(/^.*cakewalk\//, '')}` : '';
  visualPreview.src = buildVisualizerUrl(candidate);
  metaPreview.textContent = JSON.stringify(candidate, null, 2);

  editorForm.classList.remove('hidden');
  emptyEditor.classList.add('hidden');
}

function selectCandidate(id) {
  selected = candidates.find(item => item.id === id);
  renderCandidateList();
  fillEditor(selected);
}

async function loadCandidates() {
  candidates = await fetchJson('/api/candidates');
  renderCandidateList();
  if (candidates.length && !selected) {
    selectCandidate(candidates[0].id);
  } else if (selected) {
    selectCandidate(selected.id);
  }
}

editorForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  if (!selected) return;
  const payload = {
    ...(selected.config || {}),
    id: fields.itemId.value,
    repo: selected.repo,
    mp3: selected.mp3,
    vtt: selected.vtt,
    pdf: selected.pdf,
    title: fields.title.value,
    description: fields.description.value,
    visualizer: fields.visualizer.value,
    speed: Number(fields.speed.value),
    tone: Number(fields.tone.value),
    ready: fields.ready.value === 'true'
  };
  await fetchJson('/api/config', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  await loadCandidates();
});

refreshButton.addEventListener('click', loadCandidates);

loadCandidates().catch(err => {
  candidateList.innerHTML = `<div class="placeholder">Failed to load: ${err.message}</div>`;
});
