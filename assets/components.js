/* ============================================
   SOLUTIONS SENIOR – JS PARTAGÉ
   Modifier ce fichier = s'applique partout
   ============================================ */

// ── CHARGEMENT DES COMPOSANTS ──────────────────
async function loadComponent(id, file) {
  const el = document.getElementById(id);
  if (!el) return;
  try {
    const base = window.location.origin;
    const res = await fetch(base + '/components/' + file);
    const html = await res.text();
    el.innerHTML = html;
  } catch(e) {
    console.warn('Composant non chargé:', file);
  }
}

document.addEventListener('DOMContentLoaded', async () => {
  await Promise.all([
    loadHeroLocal(),
    loadComponent('site-header', 'header.html'),
    loadComponent('site-footer', 'footer.html'),
    loadComponent('site-cta', 'cta-devis.html'),
    loadComponent('bandeau-rea', 'bandeau-rea.html'),
    loadComponent('formulaire-modal', 'formulaire-devis.html'),
    loadComponent('bandeau-sticky', 'bandeau-sticky.html'),
  ]);
  initForms();
  initServiceForm();
  initTocMobile();
  initTocScroll();
  initStickyBar();
});

// ── FORMULAIRE MULTI-ÉTAPES ────────────────────
function initForms() {
  window.selectService = function(el, form) {
    el.parentNode.querySelectorAll('.service-option').forEach(o => o.classList.remove('selected'));
    el.classList.add('selected');
  };
  window.nextStep = function(form, current) {
    const p = form === 'hero' ? 'h' : 'm';
    document.getElementById(p+'step'+current).classList.remove('active');
    document.getElementById(p+'step'+(current+1)).classList.add('active');
    updateDots(form, current+1);
  };
  window.prevStep = function(form, current) {
    const p = form === 'hero' ? 'h' : 'm';
    document.getElementById(p+'step'+current).classList.remove('active');
    document.getElementById(p+'step'+(current-1)).classList.add('active');
    updateDots(form, current-1);
  };
  window.submitForm = function(form) {
    const p = form === 'hero' ? 'h' : 'm';
    for(let i=0;i<3;i++){const el=document.getElementById(p+'step'+i);if(el)el.classList.remove('active');}
    const ind = document.getElementById(form==='hero'?'heroIndicators':'modalIndicators');
    if(ind) ind.style.display='none';
    const s = document.getElementById(p+'success');
    if(s) s.classList.add('active');
  };
  window.updateDots = function(form, active) {
    const p = form === 'hero' ? 'h' : 'm';
    for(let i=0;i<3;i++){
      const d=document.getElementById(p+'dot'+i);
      if(!d) continue;
      d.className='step-dot';
      if(i<active) d.classList.add('done');
      else if(i===active) d.classList.add('active');
    }
  };
  window.openModal = function() {
    const o = document.getElementById('modalOverlay');
    if(o){ o.classList.add('open'); document.body.style.overflow='hidden'; }
  };
  window.closeModal = function() {
    const o = document.getElementById('modalOverlay');
    if(o){ o.classList.remove('open'); document.body.style.overflow=''; }
  };
  window.closeModalOutside = function(e) {
    if(e.target===document.getElementById('modalOverlay')) closeModal();
  };

  // Connecter tous les boutons .open-formulaire au modal
  document.addEventListener('click', function(e) {
    if(e.target.closest('.open-formulaire')) {
      e.preventDefault();
      if(typeof openModal === 'function') openModal();
    }
  });
}

// ── SOMMAIRE MOBILE (ACCORDÉON) ───────────────
function initTocMobile() {
  const toggle = document.querySelector('.toc-mobile-toggle');
  const content = document.querySelector('.toc-mobile-content');
  if(!toggle || !content) return;
  toggle.addEventListener('click', () => {
    toggle.classList.toggle('open');
    content.classList.toggle('open');
  });
}

// ── SOMMAIRE DESKTOP (SUIVI SCROLL) ──────────
function initTocScroll() {
  const tocLinks = document.querySelectorAll('.toc a');
  if(!tocLinks.length) return;
  const headings = document.querySelectorAll('.article-content h2, .article-content h3');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if(entry.isIntersecting) {
        tocLinks.forEach(a => a.classList.remove('active'));
        const active = document.querySelector('.toc a[href="#'+entry.target.id+'"]');
        if(active) active.classList.add('active');
      }
    });
  }, { rootMargin: '-20% 0px -70% 0px' });
  headings.forEach(h => observer.observe(h));
}

// ── BANDEAU STICKY ────────────────────────────
function initStickyBar() {
  const bar = document.getElementById('bandeau-sticky');
  if (!bar) return;

  // Personnalisation du titre selon la page (data-titre sur le div)
  const titre = bar.getAttribute('data-titre');
  const titreEl = document.getElementById('sticky-titre');
  if (titre && titreEl) titreEl.textContent = titre;

  const closeBtn = document.getElementById('sticky-bar-close');
  const ctaBtn   = document.getElementById('sticky-bar-btn');
  let closed = false;

  // Scroll : afficher après 400px
  window.addEventListener('scroll', function() {
    if (closed) return;
    if (window.scrollY > 400) {
      bar.classList.add('visible');
    } else {
      bar.classList.remove('visible');
    }
  }, { passive: true });

  // Fermer
  if (closeBtn) {
    closeBtn.addEventListener('click', function() {
      bar.classList.remove('visible');
      closed = true;
    });
  }

  // CTA → ouvre le formulaire modal
  if (ctaBtn) {
    ctaBtn.addEventListener('click', function() {
      if (typeof openModal === 'function') openModal();
    });
  }
}
function initServiceForm() {
  const service = document.body.getAttribute('data-service');
  if (!service) return;

  const services = {
    'monte-escaliers': { icon: '🪜', label: 'Monte-escalier' },
    'douche-senior':   { icon: '🛁', label: 'Douche senior' },
    'aide-domicile':   { icon: '🤝', label: 'Aide à domicile' },
    'mutuelle':        { icon: '💊', label: 'Mutuelle senior' },
    'teleassistance':  { icon: '📡', label: 'Téléassistance' },
    'residence':       { icon: '🏘️', label: 'Résidence / EHPAD' },
  };

  const s = services[service];
  if (!s) return;

  const gridFull   = document.getElementById('service-grid-full');
  const gridSingle = document.getElementById('service-grid-single');
  const serviceEl  = document.getElementById('service-unique');

  if (gridFull && gridSingle && serviceEl) {
    gridFull.style.display   = 'none';
    gridSingle.style.display = 'grid';
    serviceEl.innerHTML = '<span class="icon">' + s.icon + '</span> ' + s.label;
  }
}

// ── HERO LOCAL (pages villes) ─────────────────
// Se déclenche uniquement sur les pages avec data-ville sur le body
async function loadHeroLocal() {
  const ville   = document.body.getAttribute('data-ville');
  const dept    = document.body.getAttribute('data-dept');
  const deptNum = document.body.getAttribute('data-dept-num');
  const dateMaj = document.body.getAttribute('data-date-maj') || '';
  const h1Text  = document.body.getAttribute('data-h1') || '';
  const target  = document.getElementById('hero-local');

  if (!ville || !target) return;

  try {
    const base = window.location.origin;
    const res  = await fetch(base + '/components/formulaire-hero-local.html');
    let html   = await res.text();

    // Remplacement des variables
    html = html.split('{{VILLE}}').join(ville);
    html = html.split('{{DEPT}}').join(dept);
    html = html.split('{{DEPT_NUM}}').join(deptNum);
    html = html.split('{{DATE_MAJ}}').join(dateMaj);
    target.innerHTML = html;

    // H1 depuis data-h1
    const h1El = target.querySelector('.hero-local-h1');
    if (h1El && h1Text) h1El.innerHTML = h1Text;

    // Init tunnel avec les données de la ville
    lData = { service: 'Monte-escalier', ville: ville, departement: dept, codeRegion: deptNum };
  } catch(e) {
    console.warn('Hero local non chargé:', e);
  }
}

// ── JS TUNNEL (partagé pour toutes les pages locales) ──
var lCurrent = 0;
var lData    = {};

function lUpdateProgress(step) {
  for (var i = 0; i < 3; i++) {
    var b = document.getElementById('lbar' + i);
    if (!b) continue;
    b.className = 'lform-progress-bar';
    if (i < step) b.classList.add('done');
    else if (i === step) b.classList.add('active');
  }
}

function lGoTo(next) {
  var current = document.getElementById('lstep' + lCurrent);
  var target  = document.getElementById('lstep' + next);
  if (!target) return;
  if (next < lCurrent) { target.style.transform = 'translateX(-24px)'; }
  else { target.style.transform = 'translateX(24px)'; }
  if (current) {
    current.classList.add('leaving');
    current.classList.remove('active');
    setTimeout(function() { if (current) current.classList.remove('leaving'); }, 250);
  }
  target.classList.add('active');
  target.getBoundingClientRect();
  target.style.transform = '';
  lCurrent = next;
  lUpdateProgress(Math.min(next, 2));
}

function lSelectOption(el) {
  el.closest('.lform-grid').querySelectorAll('.lform-option-large').forEach(function(o) {
    o.classList.remove('selected');
  });
  el.classList.add('selected');
  var textEl = el.querySelector('.lform-option-text');
  lData.localisation = textEl ? textEl.textContent.trim() : el.textContent.trim();
}

function lNextStep(current) { lGoTo(current + 1); }
function lPrevStep(current) { lGoTo(current - 1); }

function lSubmit() {
  lData.codePostal = document.getElementById('lcp').value;
  lData.pour       = document.getElementById('lpour').value;
  lData.prenom     = document.getElementById('lprenom').value;
  lData.nom        = document.getElementById('lnom').value;
  lData.telephone  = document.getElementById('ltel').value;
  lData.email      = document.getElementById('lemail').value;

  if (!lData.prenom || !lData.telephone || !lData.email) {
    alert('Merci de renseigner prénom, téléphone et email.');
    return;
  }

  fetch('https://formspree.io/f/mbdpyayv', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(lData)
  });

  document.querySelector('.lform-progress').style.display = 'none';
  var step2 = document.getElementById('lstep2');
  step2.classList.add('leaving');
  step2.classList.remove('active');
  setTimeout(function() {
    step2.classList.remove('leaving');
    document.getElementById('lsuccess').classList.add('active');
  }, 250);
}
