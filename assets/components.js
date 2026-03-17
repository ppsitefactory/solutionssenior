/* ============================================
   SENIORCONFORT – JS PARTAGÉ
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

// ── ADAPTATION FORMULAIRE SELON LE SERVICE DE LA PAGE ──
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
