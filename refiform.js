/* Finch Mortgages — two-step refinance form.
   Progressive enhancement: without JavaScript every field shows and the form posts normally. */
(function () {
  'use strict';
  var d = document;

  function isRefi(type) { return !type || /refinanc/i.test(type.value); }

  function setup(form) {
    var s1 = form.querySelector('[data-step="1"]');
    var s2 = form.querySelector('[data-step="2"]');
    var next = form.querySelector('[data-step-next]');
    var back = form.querySelector('[data-step-back]');
    var label = form.querySelector('[data-step-label]');
    var type = form.querySelector('[name="enquiry_type"]');
    var refiOnly = form.querySelector('[data-refi-only]');
    var submit = form.querySelector('[type="submit"]');
    if (!s1 || !s2 || !next) return;

    function syncType() {
      var refi = isRefi(type);
      if (refiOnly) refiOnly.hidden = !refi;
      if (submit) submit.textContent = refi ? 'GET MY FREE REFINANCE CHECK →' : 'GET MY FREE ASSESSMENT →';
    }
    function show(step) {
      s1.hidden = step !== 1;
      s2.hidden = step !== 2;
      if (label) {
        label.textContent = step === 1
          ? 'Step 1 of 2 · ' + (isRefi(type) ? 'Your mortgage' : 'Your situation')
          : 'Step 2 of 2 · Where should we reply?';
      }
    }

    next.hidden = false;
    if (back) back.hidden = false;
    if (type) type.addEventListener('change', function () { syncType(); show(1); });
    syncType();
    show(1);

    next.addEventListener('click', function () {
      fillFromCalculator(form);
      show(2);
      var first = s2.querySelector('input[name="name"]');
      if (first) first.focus();
      if (typeof window.finchTrack === 'function') {
        window.finchTrack('form_step', {
          form_id: form.getAttribute('data-form-id') || '',
          step: 2,
          enquiry_type: type ? type.value : ''
        });
      }
    });
    if (back) back.addEventListener('click', function () { show(1); });

    // The required contact fields live in step 2; make sure they're visible if validation fires.
    form.addEventListener('invalid', function () { show(2); }, true);
    form.addEventListener('submit', function () { fillFromCalculator(form); }, true);
  }

  function val(id) { var el = d.getElementById(id); return el ? el.value : ''; }

  // On the refinance calculator, pass the visitor's own numbers through with the enquiry.
  function fillFromCalculator(form) {
    var balance = parseFloat(val('rs-balance'));
    if (!balance) return;
    var saving = d.getElementById('rs-monthly-save');
    var fields = {
      calc_balance: String(balance),
      calc_current_rate: val('rs-current'),
      calc_new_rate: val('rs-new'),
      calc_term_years: val('rs-term'),
      calc_monthly_saving: saving ? saving.textContent : ''
    };
    Object.keys(fields).forEach(function (k) {
      if (!fields[k]) return;
      var input = form.querySelector('input[name="' + k + '"]');
      if (!input) {
        input = d.createElement('input');
        input.type = 'hidden';
        input.name = k;
        form.appendChild(input);
      }
      input.value = fields[k];
    });
    var band = form.querySelector('select[name="loan_balance"]');
    if (band && !band.value) {
      band.value = balance < 300000 ? 'Under $300k'
        : balance < 500000 ? '$300k–$500k'
        : balance < 750000 ? '$500k–$750k'
        : balance < 1000000 ? '$750k–$1m' : 'Over $1m';
    }
  }

  function init() { Array.prototype.forEach.call(d.querySelectorAll('form[data-refi-form]'), setup); }
  if (d.readyState === 'loading') d.addEventListener('DOMContentLoaded', init);
  else init();
})();
