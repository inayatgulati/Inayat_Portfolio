#!/usr/bin/env python3
"""Adds the new Selected work list to index.html.
Run from your portfolio folder:  python3 apply_work_list.py
A backup is saved as index.backup.html first."""
import re, shutil, sys

CSS = r'''
/* ==========================================================
   SELECTED WORK — editorial list with hover preview
   Paste just before </style>. Pairs with work-list.html.
   (You can delete the bento-fix.css block; these rows don't use it.)
   ========================================================== */

#work .section-title { font-size: var(--fs-h2); line-height: 1; }
.work-hint {
  font-family: 'Reenie Beanie', cursive; font-size: 18px; color: var(--accent-red);
  transform: rotate(3deg); display: inline-block; opacity: 0.85; white-space: nowrap;
}
.work-count { font-family: var(--font-text); font-size: var(--fs-lead); color: var(--ink-faint); }

.work-list { border-top: 2px solid var(--ink); }

.work-row {
  --result-w: clamp(160px, 18vw, 280px);
  position: relative;
  display: grid;
  grid-template-columns: clamp(36px, 4vw, 64px) minmax(0, 1fr) var(--result-w) 32px;
  align-items: center;
  column-gap: clamp(16px, 2.5vw, 40px);
  padding: clamp(22px, 3vw, 40px) 0;
  border-bottom: 1.5px solid rgba(26, 22, 18, 0.35);
  color: var(--ink);
  text-decoration: none;
  transition: opacity 0.3s ease;
}

.work-num { font-family: var(--font-mono); font-size: var(--fs-ui); color: var(--ink-faint); }

.work-title {
  display: block;
  font-family: var(--font-hand);
  font-size: clamp(30px, calc(16px + 2.2vw), 76px);
  font-weight: 700; line-height: 1; letter-spacing: -0.5px;
  transition: transform 0.35s ease, color 0.35s ease;
}
.work-meta { display: block; margin-top: 10px; font-size: var(--fs-body); color: var(--ink-faint); }
.work-result { font-size: var(--fs-body); color: var(--ink); }
.work-arrow {
  justify-self: end; font-size: clamp(22px, 2vw, 34px); line-height: 1;
  transition: transform 0.3s ease, color 0.3s ease;
}

/* hover / keyboard focus: title slides, turns red, preview pins in beside it */
.work-row:hover .work-title,
.work-row:focus-visible .work-title { color: var(--accent-red); transform: translateX(14px); }
.work-row:hover .work-arrow,
.work-row:focus-visible .work-arrow { color: var(--accent-red); transform: translate(3px, -3px); }
.work-row:focus-visible { outline: 2px solid var(--accent-red); outline-offset: 4px; }
.work-list:hover .work-row:not(:hover) { opacity: 0.45; }

.work-preview {
  position: absolute; z-index: 5;
  right: calc(var(--result-w) + 32px + clamp(16px, 2.5vw, 40px) * 2);
  top: 50%;
  width: clamp(200px, 16vw, 300px); aspect-ratio: 4 / 3;
  background: var(--paper-dark);
  border: 2px solid var(--ink);
  box-shadow: 5px 6px 0 rgba(26, 22, 18, 0.18);
  overflow: hidden; pointer-events: none;
  opacity: 0; transform: translateY(-50%) rotate(-3deg) scale(0.96);
  transition: opacity 0.3s ease, transform 0.35s ease;
}
.work-row:hover .work-preview,
.work-row:focus-visible .work-preview { opacity: 1; transform: translateY(-50%) rotate(1.5deg) scale(1); }
.work-preview img, .work-preview video { width: 100%; height: 100%; object-fit: cover; display: block; }
.work-preview video { object-fit: contain; padding: 8px; }

/* touch + small screens: no hover, so show the screenshot inline */
@media (max-width: 768px), (hover: none) {
  .work-row { grid-template-columns: 32px minmax(0, 1fr) 28px; row-gap: 6px; }
  .work-result { grid-column: 2; grid-row: 2; margin-top: 4px; }
  .work-arrow { grid-column: 3; grid-row: 1; align-self: start; }
  .work-preview {
    position: static; grid-column: 1 / -1; width: 100%; margin-top: 14px;
    opacity: 1; transform: none; aspect-ratio: 16 / 10;
  }
  .work-list:hover .work-row:not(:hover) { opacity: 1; }
  .work-hint { display: none; }
}

@media (prefers-reduced-motion: reduce) {
  .work-title, .work-arrow, .work-preview, .work-row { transition: none; }
}
'''

SECTION = r'''
<section id="work" class="page-edge" style="background:var(--paper-dark)">
<div class="margin-strip"></div>
<div class="section-header">
<h2 class="section-title">Selected work</h2>
<div class="section-line"></div>
<span class="work-hint">← hover to peek</span>
<span class="work-count">(5)</span>
</div>

<div class="work-list">

<a href="./Projects/mastercard-fraud-dashboard.html" class="work-row">
<span class="work-num">01</span>
<span>
<span class="work-title">Fraud Detection Dashboard</span>
<span class="work-meta">Mastercard · Interaction Design · 2025</span>
</span>
<span class="work-result">60% less analysis time</span>
<span class="work-arrow" aria-hidden="true">↗</span>
<span class="work-preview"><img src="./Images/Chart 2.png" alt="Fraud Detection Dashboard" /></span>
</a>

<a href="./Projects/Stockflow.html" class="work-row">
<span class="work-num">02</span>
<span>
<span class="work-title">Stockflow</span>
<span class="work-meta">Devgon Industries · Product Design · 2026</span>
</span>
<span class="work-result">One connected inventory system</span>
<span class="work-arrow" aria-hidden="true">↗</span>
<span class="work-preview"><img src="./Images/stockflow_dashboard_blurred.png" alt="Stockflow inventory dashboard" /></span>
</a>

<a href="./Projects/Inscope.html" class="work-row">
<span class="work-num">03</span>
<span>
<span class="work-title">InScope</span>
<span class="work-meta">Coast Capital · UX/UI + Design System · 2026</span>
</span>
<span class="work-result">32 screens, one design system</span>
<span class="work-arrow" aria-hidden="true">↗</span>
<span class="work-preview"><video src="./Images/Inscope_1.mp4" autoplay muted loop playsinline></video></span>
</a>

<a href="./Projects/Mastercard_Project.html" class="work-row">
<span class="work-num">04</span>
<span>
<span class="work-title">Mastercard Workplace</span>
<span class="work-meta">Internship · Enterprise UX · 2025</span>
</span>
<span class="work-result">40% faster navigation</span>
<span class="work-arrow" aria-hidden="true">↗</span>
<span class="work-preview"><img src="./Images/Mastercard.png" alt="Mastercard SharePoint redesign" /></span>
</a>

<a href="./Projects/Pawth_Project.html" class="work-row">
<span class="work-num">05</span>
<span>
<span class="work-title">Pawth</span>
<span class="work-meta">Pet owner app · UX/UI · 2026</span>
</span>
<span class="work-result">Social app for pet lovers</span>
<span class="work-arrow" aria-hidden="true">↗</span>
<span class="work-preview"><video src="./Images/Pawth.mp4" autoplay muted loop playsinline></video></span>
</a>

</div>

<div class="view-all-wrap">
<a href="./Projects.html" class="view-all-link">View all projects →</a>
</div>
</section>
'''

path = "index.html"
html = open(path, encoding="utf-8").read()
shutil.copy(path, "index.backup.html")

pattern = re.compile(r'<!-- 02 · SELECTED WORK -->\s*<section id="work".*?</section>', re.S)
if not pattern.search(html):
    sys.exit("Couldn't find the Selected work section. Nothing changed.")
html = pattern.sub(lambda m: "<!-- 02 · SELECTED WORK -->\n" + SECTION.strip(), html, count=1)

if "SELECTED WORK — editorial list" not in html:
    html = html.replace("</style>", CSS + "\n</style>", 1)

open(path, "w", encoding="utf-8").write(html)
print("Done. Open index.html to check it, then git add . / commit / push.")