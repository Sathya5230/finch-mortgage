/* Finch Mortgages — lead attribution & conversion tracking.
   Standalone, no build step. Loaded on every page via <script defer src="/leadtrack.js">. */
(function () {
  'use strict';

  /* ===================================================================
     CONFIG — paste your GA4 Measurement ID below to switch GA4 on.
     Leave empty and everything else (dataLayer, Meta Pixel, attribution)
     still works; only the GA4 beacon stays dormant.
     =================================================================== */
  var GA4_ID = '';            // e.g. 'G-XXXXXXXXXX'
  var META_PIXEL_ACTIVE = true; // Meta Pixel is already initialised in each page's <head>

  var STORE_KEY = 'finch_attr_v1';
  var w = window, d = document;

  /* ---------- GA4 (only if an ID is configured) ---------- */
  w.dataLayer = w.dataLayer || [];
  function gtag() { w.dataLayer.push(arguments); }
  if (GA4_ID) {
    var g = d.createElement('script');
    g.async = true;
    g.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA4_ID;
    d.head.appendChild(g);
    gtag('js', new Date());
    gtag('config', GA4_ID, { send_page_view: true });
  }

  /* ---------- First-touch attribution, persisted across the visit ---------- */
  function readAttr() {
    try { return JSON.parse(localStorage.getItem(STORE_KEY)) || null; } catch (e) { return null; }
  }
  function captureAttr() {
    var existing = readAttr();
    var qs = new URLSearchParams(w.location.search);
    var hasUtm = qs.has('utm_source') || qs.has('gclid') || qs.has('fbclid');
    // Keep the first touch unless this visit carries fresh campaign params.
    if (existing && !hasUtm) return existing;
    var attr = {
      utm_source: qs.get('utm_source') || (existing && existing.utm_source) || '',
      utm_medium: qs.get('utm_medium') || (existing && existing.utm_medium) || '',
      utm_campaign: qs.get('utm_campaign') || (existing && existing.utm_campaign) || '',
      utm_term: qs.get('utm_term') || (existing && existing.utm_term) || '',
      gclid: qs.get('gclid') || (existing && existing.gclid) || '',
      fbclid: qs.get('fbclid') || (existing && existing.fbclid) || '',
      landing_page: (existing && existing.landing_page) || w.location.pathname,
      referrer: (existing && existing.referrer) || (d.referrer || 'direct'),
      first_seen: (existing && existing.first_seen) || new Date().toISOString()
    };
    try { localStorage.setItem(STORE_KEY, JSON.stringify(attr)); } catch (e) {}
    return attr;
  }
  var attr = captureAttr();

  /* ---------- Page context, read from the meta tags the build injects ---------- */
  function meta(name) {
    var el = d.querySelector('meta[name="' + name + '"]');
    return el ? el.getAttribute('content') : '';
  }
  var ctx = {
    page_path: w.location.pathname,
    page_title: d.title,
    service: meta('finch:service'),
    city: meta('finch:city')
  };

  /* ---------- Unified event dispatch ---------- */
  var META_MAP = { generate_lead: 'Lead', tel_click: 'Contact', email_click: 'Contact' };
  function track(name, params) {
    var payload = Object.assign({ event: name }, ctx, attr, params || {});
    w.dataLayer.push(payload);
    if (GA4_ID) gtag('event', name, payload);
    if (META_PIXEL_ACTIVE && META_MAP[name] && typeof w.fbq === 'function') {
      w.fbq('track', META_MAP[name], {
        content_name: ctx.service || ctx.page_title,
        content_category: ctx.city || 'NZ'
      });
    }
  }
  w.finchTrack = track; // callable from inline handlers if ever needed

  /* ---------- Stamp lead context onto every form so leads are attributable ---------- */
  function stampForms() {
    var fields = Object.assign({}, ctx, attr);
    Array.prototype.forEach.call(d.querySelectorAll('form'), function (form) {
      if (form.dataset.finchStamped) return;
      form.dataset.finchStamped = '1';
      Object.keys(fields).forEach(function (k) {
        if (!fields[k]) return;
        if (form.querySelector('[name="' + k + '"]')) return;
        var i = d.createElement('input');
        i.type = 'hidden';
        i.name = k;
        i.value = fields[k];
        form.appendChild(i);
      });
    });
  }

  /* ---------- Listeners ---------- */
  function onReady() {
    stampForms();

    d.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a');
      if (!a) return;
      var href = a.getAttribute('href') || '';
      if (href.indexOf('tel:') === 0) {
        track('tel_click', { lead_channel: 'phone', link_text: (a.textContent || '').trim().slice(0, 60) });
      } else if (href.indexOf('mailto:') === 0) {
        track('email_click', { lead_channel: 'email' });
      } else if (a.dataset.cta) {
        track('cta_click', { cta_id: a.dataset.cta, cta_text: (a.textContent || '').trim().slice(0, 60) });
      }
    }, true);

    d.addEventListener('submit', function (e) {
      var form = e.target;
      if (!form || form.tagName !== 'FORM') return;
      stampForms();
      var fd = new FormData(form);
      track('generate_lead', {
        lead_channel: 'form',
        form_id: form.getAttribute('data-form-id') || form.getAttribute('id') || 'contact',
        enquiry_type: fd.get('enquiry_type') || '',
        value: 1,
        currency: 'NZD'
      });
    }, true);

    // Scroll depth — tells you whether location pages are read or bounced.
    var hits = {};
    var onScroll = function () {
      var h = d.documentElement;
      var pct = (h.scrollTop + w.innerHeight) / h.scrollHeight * 100;
      [25, 50, 75, 90].forEach(function (m) {
        if (pct >= m && !hits[m]) { hits[m] = 1; track('scroll_depth', { percent: m }); }
      });
      if (hits[90]) w.removeEventListener('scroll', onScroll);
    };
    w.addEventListener('scroll', onScroll, { passive: true });

    // Calculator engagement = high-intent signal worth retargeting.
    if (/\/calculators\//.test(w.location.pathname)) {
      var fired = false;
      d.addEventListener('input', function () {
        if (fired) return;
        fired = true;
        track('calculator_use', { calculator: w.location.pathname.split('/').pop() });
      }, true);
    }
  }

  if (d.readyState === 'loading') d.addEventListener('DOMContentLoaded', onReady);
  else onReady();
})();
