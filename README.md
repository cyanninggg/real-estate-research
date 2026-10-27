# Real Estate Research

Cyan Li’s Greater Boston multifamily research portfolio, focused on real estate development and asset analysis. It includes the Hew–Harper comparison, Greystar’s Everett Triangle, interactive operating and development models, and a lease-concession calculator.

## Technology

Plain HTML, CSS and JavaScript. No framework, package install, build step, or custom GitHub Actions workflow is required. The map loads Leaflet and mapping assets from external services. `index.html` is at the repository root. The two JSON files contain the public listing dataset and source-check notes. `.nojekyll` serves the files without Jekyll processing.

## GitHub Pages

In **Settings → Pages → Build and deployment**, select:

- **Source:** Deploy from a branch
- **Branch:** main
- **Folder:** / (root)

Click **Save**. GitHub publishes subsequent pushes to `main` automatically. The site URL is `https://cyanninggg.github.io/real-estate-research/`.

Relative asset links and hash-based navigation work at the repository subpath; no base-path change is needed.

## Local preview

Run `python3 -m http.server 8000` from this folder, then open `http://localhost:8000`.

## Research scope

The analysis uses public data and stated assumptions. Estimates and scenario results are not owner-reported performance. Original research assets and financial models are preserved; the presentation and learning workspace are maintained separately.

## Phase 1 portfolio structure

The main navigation is Home (`#/`), Research (`#/research`), Methodology (`#/method`) and About / Resume (`#/about`). Existing case and analysis routes remain valid. `portfolio.js` composes the shared seven-section case narrative around the original models; `portfolio.css` supplies the editorial layout. `study.js` still manages the map and source loading.

Phase 1 changes information architecture only. Existing numerical conclusions are **Needs Review**, explicit modeling inputs are **Assumption**, and missing evidence is **Missing**. No financial audit or data correction is implied. See `docs/phase-1-architecture.md`, `docs/data-review-inventory.csv`, and `docs/research-backlog.md`. `docs/preserved-assets.json` records baseline dataset and model hashes.

## Research presentation and Learning Lab

The portfolio now uses an eight-section, answer-first report template. `research-components.js` provides original decision, issue-tree and policy components. Existing data and models remain provisional and unchanged.

Open `#/lab` for the separate Analyst Learning Lab. `lab-content.js`, `lab.js` and `lab.css` supply lessons, practice, review tools, research questions, career prompts and browser-local progress. The route is public; user notes stay in that browser and are not synced or published. Use the progress page to export/import JSON. Three foundational lessons are authored; additional framework lessons are labeled outlines. See `docs/phase-2-implementation.md` for scope and reference-design boundaries.

No build step is required. Run the relevant checks from the repository root:

```sh
node tests/lab-state.test.cjs
node tests/research-integrity.test.cjs
```

The integrity manifest intentionally protects the original research files. A future, separately scoped data correction must deliberately update the source record and tests rather than silently replacing assumptions.

## Reconciled model — 26 October 2026

Hew operating/development views and the Brighton study display results from the privately supplied reconciled model. Only webpage presentation results and assumptions are published. The latest Excel workbook and cell-value export are not published or offered for download. Historical lease comparisons and Everett data remain unchanged. Superseded abatement estimates are removed; sensitivity uses the supplied market-rate scenarios.

## Final Hew research revision

The Hew report uses six sections: question, analytical framework, evidence, financial analysis, findings, and sources. The existing study and Hew URLs resolve to this shared report; historical October samples and regional mapping remain available within the evidence section. `hew-report.js` renders the report, `hew-report.css` adds scoped presentation rules, and `reconciled-model.js` contains curated public figures and explanations.

The latest source workbook stays private and is not offered for download. Boston FY2026 parcel and tax fields are reported separately from the hypothetical development model. The base scenario excludes unconfirmed owner internet income and procurement cost. Broker commissions and replacement reserve remain below NOI. The fourth sensitivity view varies broker participation.

Validation: `node tests/reconciled-model.test.cjs`, `node tests/research-integrity.test.cjs`, and `node tests/lab-state.test.cjs`. The first test independently recalculates public scenarios and optionally compares them to a private local source export if available; it runs without that export. No build step is required.
