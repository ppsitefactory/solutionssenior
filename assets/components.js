/* ============================================
   SOLUTIONS SENIOR – JS PARTAGÉ
   Modifier ce fichier = s'applique partout
   ============================================ */

// ── CHARGEMENT DES COMPOSANTS ─────────────────
async function loadComponent(id, file) {
  const el = document.getElementById(id);
  if (!el) return;
  try {
    const res = await fetch(window.location.origin + '/components/' + file);
    el.innerHTML = await res.text();
  } catch(e) {
    console.warn('Composant non chargé:', file);
  }
}

document.addEventListener('DOMContentLoaded', async () => {
  await Promise.all([
    loadHeroLocal(),
    loadComponent('site-header',     'header.html'),
    loadComponent('site-footer',     'footer.html'),
    loadComponent('site-cta',        'cta-devis.html'),
    loadComponent('bandeau-rea',     'bandeau-rea.html'),
    loadComponent('formulaire-modal','formulaire-devis.html'),
    loadComponent('bandeau-sticky',  'bandeau-sticky.html'),
  ]);
  initForms();
  initTocMobile();
  initTocScroll();
  initStickyBar();
});

// ── MODAL : OPEN / CLOSE ──────────────────────
function initForms() {
  window.openModal = function() {
    initModal(); // configure le bon mode avant d'afficher
    const o = document.getElementById('modalOverlay');
    if (o) { o.classList.add('open'); document.body.style.overflow = 'hidden'; }
  };
  window.closeModal = function() {
    const o = document.getElementById('modalOverlay');
    if (o) { o.classList.remove('open'); document.body.style.overflow = ''; }
  };
  window.closeModalOutside = function(e) {
    if (e.target === document.getElementById('modalOverlay')) closeModal();
  };
  // Tous les boutons .open-formulaire ouvrent le modal
  document.addEventListener('click', function(e) {
    if (e.target.closest('.open-formulaire')) {
      e.preventDefault();
      if (typeof openModal === 'function') openModal();
    }
  });
}

// ── MODAL : INITIALISATION PAR MODE ──────────
function initModal() {
  const ville   = document.body.getAttribute('data-ville');
  const service = document.body.getAttribute('data-service');
  const isMonte = service === 'monte-escaliers';
  const dept    = document.body.getAttribute('data-dept') || '';
  const deptNum = document.body.getAttribute('data-dept-num') || '';

  const modeMonte   = document.getElementById('m-mode-monte');
  const modeGeneric = document.getElementById('m-mode-generic');
  if (!modeMonte || !modeGeneric) return;

  if (isMonte) {
    // ── Mode monte / local ──
    modeMonte.style.display   = 'block';
    modeGeneric.style.display = 'none';

    // Textes adaptés selon présence de ville
    const villePrefix = ville ? ' à ' + ville : '';
    document.getElementById('m-monte-title').textContent =
      'Votre devis gratuit' + villePrefix;
    document.getElementById('m-monte-subtitle').textContent =
      '2 minutes suffisent. Un installateur agréé' + villePrefix + ' vous rappelle sous 24h.';
    document.getElementById('m-reassurance-1').textContent =
      'Un installateur agréé' + villePrefix + ' vous rappelle sous 24h';
    document.getElementById('m-success-text').innerHTML =
      'Un installateur agréé' + villePrefix + ' vous contactera dans les <strong>24 heures</strong>. Merci de votre confiance.';

    // Données initiales du tunnel
    mData    = { service: 'Monte-escalier', ville: ville || '', departement: dept, codeRegion: deptNum };
    mCurrent = 0;

    // Reset steps
    document.querySelectorAll('#m-mode-monte .lform-step').forEach(s => {
      s.classList.remove('active', 'leaving');
    });
    document.getElementById('mstep0').classList.add('active');
    mUpdateBars(0);

  } else {
    // ── Mode générique ──
    modeMonte.style.display   = 'none';
    modeGeneric.style.display = 'block';

    gData            = {};
    gCurrent         = 0;
    gSelectedService = '';
    gPrevMap         = {};

    // Reset steps
    document.querySelectorAll('#m-mode-generic .step').forEach(s => {
      s.classList.remove('active');
    });
    document.getElementById('gstep0').classList.add('active');
    gUpdateDots(0);
  }
}

// ══════════════════════════════════════════════
// TUNNEL MODAL MONTE / LOCAL  (prefix m)
// ══════════════════════════════════════════════
var mCurrent = 0;
var mData    = {};

function mUpdateBars(step) {
  for (var i = 0; i < 3; i++) {
    var b = document.getElementById('mbar' + i);
    if (!b) continue;
    b.className = 'lform-progress-bar';
    if (i < step) b.classList.add('done');
    else if (i === step) b.classList.add('active');
  }
}

function mGoTo(next) {
  var curr = document.getElementById('mstep' + mCurrent);
  var tgt  = document.getElementById('mstep' + next);
  if (!tgt) { tgt = document.getElementById('msuccess'); }
  if (!tgt) return;

  tgt.style.transform = next > mCurrent ? 'translateX(24px)' : 'translateX(-24px)';
  if (curr) {
    curr.classList.add('leaving');
    curr.classList.remove('active');
    setTimeout(function() { if (curr) curr.classList.remove('leaving'); }, 250);
  }
  tgt.classList.add('active');
  tgt.getBoundingClientRect();
  tgt.style.transform = '';
  mCurrent = next;
  mUpdateBars(Math.min(next, 2));
}

function mSelectOption(el) {
  el.closest('.lform-grid').querySelectorAll('.lform-option-large').forEach(function(o) {
    o.classList.remove('selected');
  });
  el.classList.add('selected');
  var textEl = el.querySelector('.lform-option-text');
  mData.localisation = textEl ? textEl.textContent.trim() : el.textContent.trim();
}


// ── VALIDATION : feedback visuel ──────────────
function showError(el, type) {
  if (type === 'options') {
    // Bordure rouge sur les options non sélectionnées
    el.querySelectorAll('.lform-option-large').forEach(function(o) {
      if (!o.classList.contains('selected')) {
        o.style.borderColor = '#e05555';
      }
    });
    setTimeout(function() {
      el.querySelectorAll('.lform-option-large').forEach(function(o) {
        o.style.borderColor = '';
      });
    }, 1500);
  } else if (type === 'input') {
    el.style.borderColor = '#e05555';
    el.focus();
    setTimeout(function() { el.style.borderColor = ''; }, 1500);
  }
}

function mNextStep(current) {
  if (current === 0) {
    var sel = document.querySelector('#mstep0 .lform-option-large.selected');
    if (!sel) { showError(document.getElementById('mstep0'), 'options'); return; }
  }
  if (current === 1) {
    var cp = document.getElementById('m-cp');
    if (!cp.value.trim()) { showError(cp, 'input'); return; }
  }
  mGoTo(current + 1);
}
function mPrevStep(current) { mGoTo(current - 1); }

function mSubmit() {
  mData.codePostal = document.getElementById('m-cp').value;
  mData.pour       = document.getElementById('m-pour').value;
  mData.prenom     = document.getElementById('m-prenom').value;
  mData.nom        = document.getElementById('m-nom').value;
  mData.telephone  = document.getElementById('m-tel').value;
  mData.email      = document.getElementById('m-email').value;

  var ok = true;
  ['m-prenom','m-tel','m-email'].forEach(function(id) {
    var el = document.getElementById(id);
    if (el && !el.value.trim()) { showError(el, 'input'); ok = false; }
  });
  if (!ok) return;
  fetch('https://formspree.io/f/mbdpyayv', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(mData)
  });

  document.getElementById('m-monte-progress').style.display = 'none';
  var step2 = document.getElementById('mstep2');
  step2.classList.add('leaving');
  step2.classList.remove('active');
  setTimeout(function() {
    step2.classList.remove('leaving');
    document.getElementById('msuccess').classList.add('active');
  }, 250);
}

// ══════════════════════════════════════════════
// TUNNEL MODAL GÉNÉRIQUE  (prefix g)
// ══════════════════════════════════════════════
var gCurrent         = 0;
var gData            = {};
var gSelectedService = ''; // 'monte' | 'other' | 'interior' | 'exterior'
var gPrevMap         = {}; // pour le bouton Retour lors des sauts d'étapes

function gUpdateDots(step) {
  for (var i = 0; i < 4; i++) {
    var d = document.getElementById('gdot' + i);
    if (!d) continue;
    d.className = 'step-dot';
    if (i < step) d.classList.add('done');
    else if (i === step) d.classList.add('active');
  }
}

function gGoTo(next, from) {
  var curr = document.getElementById('gstep' + gCurrent) ||
             document.getElementById('gsuccess');
  var tgt  = document.getElementById('gstep' + next) ||
             document.getElementById('gsuccess');
  if (!tgt) return;

  gPrevMap[next] = from !== undefined ? from : gCurrent;
  tgt.style.transform = next > gCurrent ? 'translateX(24px)' : 'translateX(-24px)';
  if (curr) { curr.classList.remove('active'); }
  tgt.classList.add('active');
  tgt.getBoundingClientRect();
  tgt.style.transform = '';
  gCurrent = next;
  gUpdateDots(Math.min(next, 3));
}

function gSelectService(el, type) {
  el.parentNode.querySelectorAll('.service-option').forEach(function(o) {
    o.classList.remove('selected');
  });
  el.classList.add('selected');
  gData.service    = el.textContent.trim();
  gSelectedService = type;
}

function gNextStep(current) {
  if (current === 0) {
    if (gSelectedService === 'monte') {
      gGoTo(1, 0);
    } else {
      gGoTo(2, 0);
    }
  } else if (current === 2) {
    var cp = document.getElementById('g-cp');
    if (!cp.value.trim()) { showError(cp, 'input'); return; }
    gGoTo(3, 2);
  } else {
    gGoTo(current + 1, current);
  }
}

function gPrevStep(current) {
  var prev = gPrevMap[current] !== undefined ? gPrevMap[current] : current - 1;
  gGoTo(prev, current);
}

function gSubmit() {
  gData.codePostal = document.getElementById('g-cp').value;
  gData.pour       = document.getElementById('g-pour').value;
  gData.prenom     = document.getElementById('g-prenom').value;
  gData.nom        = document.getElementById('g-nom').value;
  gData.email      = document.getElementById('g-email').value;
  gData.telephone  = document.getElementById('g-tel').value;

  var ok = true;
  ['g-prenom','g-tel','g-email'].forEach(function(id) {
    var el = document.getElementById(id);
    if (el && !el.value.trim()) { showError(el, 'input'); ok = false; }
  });
  if (!ok) return;
  fetch('https://formspree.io/f/mbdpyayv', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(gData)
  });

  document.querySelector('#m-mode-generic .step-indicators').style.display = 'none';
  document.getElementById('gstep3').classList.remove('active');
  document.getElementById('gsuccess').classList.add('active');
}

// ══════════════════════════════════════════════
// TUNNEL HERO LOCAL / MONTE  (prefix l)
// ══════════════════════════════════════════════
var lCurrent = 0;
var lData    = {};

function lUpdateBars(step) {
  for (var i = 0; i < 3; i++) {
    var b = document.getElementById('lbar' + i);
    if (!b) continue;
    b.className = 'lform-progress-bar';
    if (i < step) b.classList.add('done');
    else if (i === step) b.classList.add('active');
  }
}

function lGoTo(next) {
  var curr = document.getElementById('lstep' + lCurrent);
  var tgt  = document.getElementById('lstep' + next);
  if (!tgt) { tgt = document.getElementById('lsuccess'); }
  if (!tgt) return;

  tgt.style.transform = next > lCurrent ? 'translateX(24px)' : 'translateX(-24px)';
  if (curr) {
    curr.classList.add('leaving');
    curr.classList.remove('active');
    setTimeout(function() { if (curr) curr.classList.remove('leaving'); }, 250);
  }
  tgt.classList.add('active');
  tgt.getBoundingClientRect();
  tgt.style.transform = '';
  lCurrent = next;
  lUpdateBars(Math.min(next, 2));
}

function lSelectOption(el) {
  el.closest('.lform-grid').querySelectorAll('.lform-option-large').forEach(function(o) {
    o.classList.remove('selected');
  });
  el.classList.add('selected');
  var textEl = el.querySelector('.lform-option-text');
  lData.localisation = textEl ? textEl.textContent.trim() : el.textContent.trim();
}

function lNextStep(current) {
  if (current === 0) {
    var sel = document.querySelector('#lstep0 .lform-option-large.selected');
    if (!sel) { showError(document.getElementById('lstep0'), 'options'); return; }
  }
  if (current === 1) {
    var cp = document.getElementById('lcp');
    if (!cp.value.trim()) { showError(cp, 'input'); return; }
  }
  lGoTo(current + 1);
}
function lPrevStep(current) { lGoTo(current - 1); }

function lSubmit() {
  lData.codePostal = document.getElementById('lcp').value;
  lData.pour       = document.getElementById('lpour').value;
  lData.prenom     = document.getElementById('lprenom').value;
  lData.nom        = document.getElementById('lnom').value;
  lData.telephone  = document.getElementById('ltel').value;
  lData.email      = document.getElementById('lemail').value;

  var ok = true;
  ['lprenom','ltel','lemail'].forEach(function(id) {
    var el = document.getElementById(id);
    if (el && !el.value.trim()) { showError(el, 'input'); ok = false; }
  });
  if (!ok) return;
  fetch('https://formspree.io/f/mbdpyayv', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(lData)
  });

  var heroProgress = document.querySelector('#hero-local .lform-progress');
  if (heroProgress) heroProgress.style.display = 'none';
  var step2 = document.getElementById('lstep2');
  step2.classList.add('leaving');
  step2.classList.remove('active');
  setTimeout(function() {
    step2.classList.remove('leaving');
    document.getElementById('lsuccess').classList.add('active');
  }, 250);
}

// ── CHARGEMENT HERO LOCAL / MONTE ─────────────
async function loadHeroLocal() {
  const ville    = document.body.getAttribute('data-ville');
  const service  = document.body.getAttribute('data-service');
  const isMonte  = service === 'monte-escaliers';
  const target   = document.getElementById('hero-local');

  // Charger uniquement sur les pages monte-escalier avec le conteneur hero-local
  if (!isMonte || !target) return;

  const dept    = document.body.getAttribute('data-dept')     || '';
  const deptNum = document.body.getAttribute('data-dept-num') || '';
  const dateMaj = document.body.getAttribute('data-date-maj') || '';
  const h1Text  = document.body.getAttribute('data-h1')       || '';

  try {
    const res  = await fetch(window.location.origin + '/components/formulaire-hero-local.html');
    let html   = await res.text();

    // Variable {{VILLE_PREFIX}} : " à Lyon" ou "" si pas de ville
    const villePrefix = ville ? ' à ' + ville : '';
    html = html.split('{{VILLE_PREFIX}}').join(villePrefix);
    html = html.split('{{VILLE}}').join(ville || '');
    html = html.split('{{DEPT}}').join(dept);
    html = html.split('{{DEPT_NUM}}').join(deptNum);
    html = html.split('{{DATE_MAJ}}').join(dateMaj);

    // Blocs conditionnels {{IF_VILLE}}...{{/IF_VILLE}}
    if (ville) {
      html = html.replace(/{{IF_VILLE}}/g, '').replace(/{{\/IF_VILLE}}/g, '');
    } else {
      html = html.replace(/{{IF_VILLE}}[\s\S]*?{{\/IF_VILLE}}/g, '');
    }

    target.innerHTML = html;

    // H1 depuis data-h1
    const h1El = target.querySelector('.hero-local-h1');
    if (h1El && h1Text) h1El.innerHTML = h1Text;

    // Init données du tunnel hero
    lData    = { service: 'Monte-escalier', ville: ville || '', departement: dept, codeRegion: deptNum };
    lCurrent = 0;

  } catch(e) {
    console.warn('Hero local non chargé:', e);
  }
}

// ── SOMMAIRE MOBILE ───────────────────────────
function initTocMobile() {
  const toggle  = document.querySelector('.toc-mobile-toggle');
  const content = document.querySelector('.toc-mobile-content');
  if (!toggle || !content) return;
  toggle.addEventListener('click', () => {
    toggle.classList.toggle('open');
    content.classList.toggle('open');
  });
}

// ── SOMMAIRE DESKTOP (SCROLL) ─────────────────
function initTocScroll() {
  const tocLinks = document.querySelectorAll('.toc a');
  if (!tocLinks.length) return;
  const headings = document.querySelectorAll('.article-content h2, .article-content h3');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        tocLinks.forEach(a => a.classList.remove('active'));
        const active = document.querySelector('.toc a[href="#' + entry.target.id + '"]');
        if (active) active.classList.add('active');
      }
    });
  }, { rootMargin: '-20% 0px -70% 0px' });
  headings.forEach(h => observer.observe(h));
}

// ── BANDEAU STICKY ────────────────────────────
function initStickyBar() {
  const bar = document.getElementById('bandeau-sticky');
  if (!bar) return;

  const titre   = bar.getAttribute('data-titre');
  const titreEl = document.getElementById('sticky-titre');
  if (titre && titreEl) titreEl.textContent = titre;

  const closeBtn = document.getElementById('sticky-bar-close');
  const ctaBtn   = document.getElementById('sticky-bar-btn');
  let closed     = false;

  window.addEventListener('scroll', function() {
    if (closed) return;
    bar.classList.toggle('visible', window.scrollY > 400);
  }, { passive: true });

  if (closeBtn) {
    closeBtn.addEventListener('click', function() {
      bar.classList.remove('visible');
      closed = true;
    });
  }
  if (ctaBtn) {
    ctaBtn.addEventListener('click', function() {
      if (typeof openModal === 'function') openModal();
    });
  }
}
