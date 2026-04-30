# First Home Buyers Landing Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Redesign `first-home-buyers.html` as a focused two-column conversion landing page with no footer.

**Architecture:** Single self-contained HTML file. Page-specific styles live in an inline `<style>` block. The existing shared header (`#main-header`, mobile menu, `style.css`) is kept unchanged. No footer. Right column has a sticky booking form; left column carries all trust/social-proof content.

**Tech Stack:** Static HTML, inline CSS, no JS framework. Tailwind CDN loaded at bottom (same as rest of site) for nav compatibility only.

---

### Task 1: Replace page-specific styles

**Files:**
- Modify: `first-home-buyers.html` — replace the existing `<style>` block inside `<section>` with a new `<style>` block in `<head>`

- [ ] **Step 1: Remove the old inline `<style>` block**

Delete everything from line `<style>` through `</style>` that currently sits inside `<section style="padding:3rem 0 5rem;">`. It starts with `.lp {` and ends before `<div class="lp">`.

- [ ] **Step 2: Add the new `<style>` block in `<head>`, just before `</head>`**

```html
<style>
/* ── Landing page layout ── */
.lp-wrap {
  max-width: 1100px;
  margin: 0 auto;
  padding: 3rem 1.5rem 5rem;
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 3rem;
  align-items: start;
}
.lp-left { display: flex; flex-direction: column; gap: 2rem; }
.lp-right { position: sticky; top: 100px; }

/* ── Eyebrow ── */
.lp-eyebrow {
  display: inline-block;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--finch-gold);
  background: rgba(178,147,97,0.1);
  padding: 5px 12px;
  border-radius: 20px;
  margin-bottom: 0.5rem;
}

/* ── Hero text ── */
.lp-h1 {
  font-family: var(--font-display);
  font-size: clamp(1.75rem, 3.5vw, 2.6rem);
  font-weight: 700;
  color: var(--neutral-black);
  line-height: 1.2;
  margin-bottom: 0.75rem;
}
.lp-sub {
  font-size: 1rem;
  color: var(--neutral-medGray);
  line-height: 1.7;
}

/* ── Bullet list ── */
.lp-bullets { list-style: none; display: flex; flex-direction: column; gap: 10px; }
.lp-bullets li {
  display: flex; align-items: flex-start; gap: 10px;
  font-size: 15px; color: var(--neutral-black); line-height: 1.5;
}
.lp-chk {
  width: 20px; height: 20px; min-width: 20px;
  background: var(--finch-forest); border-radius: 50%;
  display: flex; align-items: center; justify-content: center; margin-top: 1px;
}
.lp-chk svg { width: 10px; height: 10px; }

/* ── Trust bar ── */
.lp-trust {
  display: flex; flex-wrap: wrap; gap: 12px;
  background: var(--finch-mist);
  border: 0.5px solid rgba(98,162,154,0.3);
  border-radius: 10px;
  padding: 14px 18px;
}
.lp-trust-item {
  display: flex; align-items: center; gap: 7px;
  font-size: 13px; color: var(--neutral-medGray);
}
.lp-tdot {
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--finch-gold); flex-shrink: 0;
}

/* ── Founder card ── */
.lp-founder {
  display: flex; gap: 20px; align-items: flex-start;
  background: #fff;
  border: 0.5px solid rgba(98,162,154,0.3);
  border-radius: 14px;
  padding: 24px;
}
.lp-founder-photo {
  width: 80px; height: 80px; min-width: 80px; border-radius: 50%;
  background: var(--finch-mist);
  border: 2px solid var(--finch-sage);
  display: flex; align-items: center; justify-content: center;
  overflow: hidden;
}
.lp-founder-photo svg { width: 44px; height: 44px; }
.lp-founder-info { flex: 1; }
.lp-founder-name { font-size: 16px; font-weight: 600; color: var(--neutral-black); margin-bottom: 2px; }
.lp-founder-title { font-size: 12px; color: var(--finch-sage); margin-bottom: 10px; }
.lp-founder-bio { font-size: 13px; color: var(--neutral-medGray); line-height: 1.65; margin-bottom: 12px; }
.lp-founder-stats { display: flex; gap: 18px; }
.lp-stat-num { font-size: 17px; font-weight: 600; color: var(--finch-sage); }
.lp-stat-label { font-size: 11px; color: var(--neutral-medGray); }

/* ── Section block ── */
.lp-section {
  background: #fff;
  border: 0.5px solid rgba(98,162,154,0.3);
  border-radius: 14px;
  padding: 28px;
}
.lp-section h2 {
  font-size: 18px; font-weight: 600;
  color: var(--neutral-black); margin-bottom: 16px;
}

/* ── Testimonials ── */
.lp-tcard {
  background: var(--finch-mist);
  border-radius: 10px;
  padding: 16px 18px;
  margin-bottom: 10px;
}
.lp-tcard:last-child { margin-bottom: 0; }
.lp-tcard p {
  font-size: 14px; color: var(--neutral-black);
  line-height: 1.65; margin-bottom: 8px;
  font-family: var(--font-display, Georgia, serif);
}
.lp-tname { font-size: 12px; color: var(--neutral-medGray); font-weight: 600; }

/* ── FAQ ── */
.lp-faq-item {
  border-bottom: 0.5px solid rgba(98,162,154,0.25);
  padding: 14px 0;
}
.lp-faq-item:first-child { padding-top: 0; }
.lp-faq-item:last-child { border-bottom: none; padding-bottom: 0; }
.lp-faq-q { font-size: 14px; font-weight: 600; color: var(--neutral-black); margin-bottom: 6px; }
.lp-faq-a { font-size: 13px; color: var(--neutral-medGray); line-height: 1.65; }

/* ── Text CTA ── */
.lp-text-cta {
  font-size: 15px; font-weight: 600;
  color: var(--finch-forest);
  text-decoration: none;
  display: inline-flex; align-items: center; gap: 6px;
}
.lp-text-cta:hover { text-decoration: underline; }

/* ── Sticky form card ── */
.lp-form-card {
  background: #fff;
  border: 0.5px solid rgba(98,162,154,0.35);
  border-radius: 16px;
  padding: 28px 24px 22px;
  box-shadow: 0 4px 24px rgba(16,68,62,0.08);
}
.lp-form-title { font-size: 16px; font-weight: 600; color: var(--neutral-black); margin-bottom: 18px; }
.lp-field { margin-bottom: 12px; }
.lp-field label { display: block; font-size: 12px; color: var(--neutral-medGray); margin-bottom: 5px; }
.lp-field input,
.lp-field select {
  width: 100%; height: 40px; padding: 0 11px;
  border: 0.5px solid rgba(98,162,154,0.5);
  border-radius: 8px;
  font-size: 14px; color: var(--neutral-black);
  background: #fff;
  font-family: var(--font-sans, system-ui, sans-serif);
  box-sizing: border-box;
}
.lp-field input:focus,
.lp-field select:focus {
  outline: none;
  border-color: var(--finch-sage);
  box-shadow: 0 0 0 3px rgba(98,162,154,0.15);
}
.lp-submit {
  width: 100%; padding: 13px;
  background: var(--finch-gold); color: #fff;
  border: none; border-radius: 9px;
  font-size: 15px; font-weight: 600;
  cursor: pointer; margin-top: 14px;
  font-family: var(--font-sans, system-ui, sans-serif);
  transition: background 0.2s;
}
.lp-submit:hover { background: #9e7f52; }
.lp-form-note {
  font-size: 11px; color: var(--neutral-medGray);
  text-align: center; margin-top: 10px; line-height: 1.5;
}

/* ── Mobile ── */
@media (max-width: 768px) {
  .lp-wrap {
    grid-template-columns: 1fr;
    padding: 1.5rem 1rem 4rem;
    gap: 1.75rem;
  }
  .lp-right { position: static; order: -1; }
  .lp-founder { flex-direction: column; align-items: center; text-align: center; }
  .lp-founder-stats { justify-content: center; }
}
</style>
```

- [ ] **Step 3: Verify the file still opens in a browser without layout breakage before continuing**

Open `first-home-buyers.html` in a browser. The nav should render. The page content below it may look unstyled — that's expected at this step since the body HTML hasn't been replaced yet.

---

### Task 2: Replace the body content

**Files:**
- Modify: `first-home-buyers.html` — replace everything between `<main style="padding-top:80px;">` and `</main>`

- [ ] **Step 1: Replace the entire `<main>` body with the new two-column layout**

```html
<main style="padding-top:80px;">
<div class="lp-wrap">

  <!-- ── LEFT COLUMN ── -->
  <div class="lp-left">

    <!-- Hero -->
    <div>
      <span class="lp-eyebrow">First Home Buyers · Auckland</span>
      <h1 class="lp-h1">Still renting in Auckland?<br>You might be closer to your first home than you think.</h1>
      <p class="lp-sub">One free 15-minute call could show you exactly where you stand — no bank appointments, no jargon.</p>
    </div>

    <!-- Bullets -->
    <ul class="lp-bullets">
      <li>
        <span class="lp-chk"><svg viewBox="0 0 10 10" fill="none"><polyline points="2,5 4,7.5 8,3" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
        Find out how much you may be able to borrow — right now
      </li>
      <li>
        <span class="lp-chk"><svg viewBox="0 0 10 10" fill="none"><polyline points="2,5 4,7.5 8,3" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
        Understand whether your deposit is enough (and what to do if it's not)
      </li>
      <li>
        <span class="lp-chk"><svg viewBox="0 0 10 10" fill="none"><polyline points="2,5 4,7.5 8,3" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
        Walk away with a clear, honest plan — not a sales pitch
      </li>
    </ul>

    <!-- Trust bar -->
    <div class="lp-trust">
      <div class="lp-trust-item"><span class="lp-tdot"></span>Free &amp; confidential</div>
      <div class="lp-trust-item"><span class="lp-tdot"></span>4.9-star rated</div>
      <div class="lp-trust-item"><span class="lp-tdot"></span>500+ Auckland families helped</div>
      <div class="lp-trust-item"><span class="lp-tdot"></span>FSPR registered</div>
    </div>

    <!-- Founder card -->
    <div class="lp-founder">
      <div class="lp-founder-photo">
        <svg viewBox="0 0 52 52" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="26" cy="20" r="10" fill="var(--finch-gold)"/>
          <ellipse cx="26" cy="42" rx="16" ry="10" fill="var(--finch-gold)"/>
        </svg>
      </div>
      <div class="lp-founder-info">
        <div class="lp-founder-name">Mukhtar Kiyani</div>
        <div class="lp-founder-title">Founder &amp; Mortgage Adviser, Finch Mortgage</div>
        <div class="lp-founder-bio">I started Finch Mortgage because I watched too many Auckland families get lost in bank processes and walk away thinking they couldn't buy. I've helped hundreds of first home buyers get clear answers — and get their keys faster than they expected.</div>
        <div class="lp-founder-stats">
          <div><div class="lp-stat-num">500+</div><div class="lp-stat-label">Families helped</div></div>
          <div><div class="lp-stat-num">4.9★</div><div class="lp-stat-label">Google rating</div></div>
          <div><div class="lp-stat-num">$0</div><div class="lp-stat-label">Broker fee</div></div>
        </div>
      </div>
    </div>

    <!-- Testimonials -->
    <div class="lp-section">
      <h2>What clients say</h2>
      <div class="lp-tcard">
        <p>"We'd been to two banks and hit dead ends. One call with Finch and we had a clear plan. Three months later we had our keys."</p>
        <div class="lp-tname">James &amp; Mere — bought in Manurewa</div>
      </div>
      <div class="lp-tcard">
        <p>"I thought we were at least a year away. After one call we understood exactly where we stood and moved much faster than expected."</p>
        <div class="lp-tname">Sarah &amp; Tom — first home buyers, Papakura</div>
      </div>
      <div class="lp-tcard">
        <p>"Completely stress-free. They handled everything and got us a rate the bank wouldn't give us directly."</p>
        <div class="lp-tname">Priya M. — Manukau</div>
      </div>
    </div>

    <!-- FAQ -->
    <div class="lp-section">
      <h2>Common questions</h2>
      <div class="lp-faq-item">
        <div class="lp-faq-q">Is the consultation really free?</div>
        <div class="lp-faq-a">Yes, completely free. We're paid by the lender when your mortgage settles — not by you. You pay nothing, ever, for our advice.</div>
      </div>
      <div class="lp-faq-item">
        <div class="lp-faq-q">What if I'm not ready to buy yet?</div>
        <div class="lp-faq-a">That's absolutely fine. Knowing where you stand now means when you are ready, you're not starting from zero. Many clients book this call 6–12 months before they plan to buy.</div>
      </div>
      <div class="lp-faq-item">
        <div class="lp-faq-q">What if my deposit is small?</div>
        <div class="lp-faq-a">There are low-deposit options, Kāinga Ora First Home Loan schemes, and lender policies many people don't know about. You may have more options than you think.</div>
      </div>
    </div>

    <!-- Text CTA -->
    <a href="contact.html" class="lp-text-cta">Ready to start? Book your free call →</a>

  </div><!-- /lp-left -->

  <!-- ── RIGHT COLUMN (sticky form) ── -->
  <div class="lp-right">
    <div class="lp-form-card">
      <div class="lp-form-title">Book your free 15-minute call</div>
      <div class="lp-field">
        <label>First name</label>
        <input type="text" placeholder="Sarah" />
      </div>
      <div class="lp-field">
        <label>Mobile number</label>
        <input type="text" placeholder="021 000 0000" />
      </div>
      <div class="lp-field">
        <label>Auckland suburb</label>
        <input type="text" placeholder="e.g. Papakura" />
      </div>
      <div class="lp-field">
        <label>Buying timeline</label>
        <select>
          <option value="">Select...</option>
          <option>Within 3 months</option>
          <option>3–6 months</option>
          <option>6–12 months</option>
          <option>Just exploring</option>
        </select>
      </div>
      <button class="lp-submit">Yes — show me my options →</button>
      <div class="lp-form-note">Free · No obligation · FSPR registered</div>
    </div>
  </div><!-- /lp-right -->

</div><!-- /lp-wrap -->
</main>
```

- [ ] **Step 2: Remove the old `<script>` calculator block**

Delete the `<script>` block that references `hero-price`, `hero-deposit`, `hero-dep-val`, `hero-result` — these elements no longer exist in the new HTML. The block starts with `// Hero calculator` and ends with `calcHero();`. Keep the `tailwind.config` script and `script.js` reference.

- [ ] **Step 3: Verify in browser**

Open `first-home-buyers.html`. Check:
- Nav renders correctly at top
- Two columns appear side by side on desktop
- Sticky form stays visible while scrolling left column
- On mobile (resize to < 768px): single column, form appears above headline
- No footer visible

- [ ] **Step 4: Commit**

```bash
git add "first-home-buyers.html" "docs/superpowers/specs/2026-04-30-first-home-buyers-landing-page-design.md" "docs/superpowers/plans/2026-04-30-first-home-buyers-landing-page.md"
git commit -m "feat: redesign first-home-buyers as focused conversion landing page"
```
