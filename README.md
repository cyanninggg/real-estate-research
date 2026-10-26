# Real Estate Research

Cyan Li’s Greater Boston multifamily research portfolio, focused on real estate development and asset analysis. It includes the Hew–Harper comparison, Greystar’s Everett Triangle, interactive operating and development models, and a lease-concession calculator.

## Technology

Plain HTML, CSS and JavaScript. No dependencies, framework, build step, or custom GitHub Actions workflow is required. `index.html` is at the repository root. The two JSON files contain the public listing dataset and source-check notes. `.nojekyll` serves the files without Jekyll processing.

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

The analysis uses public data and stated assumptions. Estimates and scenario results are not owner-reported performance. The exported website files are unchanged from the current site.

## Phase 1 portfolio structure

The main navigation is Home (`#/`), Research (`#/research`), Methodology (`#/method`) and About / Resume (`#/about`). Existing case and analysis routes remain valid. `portfolio.js` composes the shared seven-section case narrative around the original models; `portfolio.css` supplies the editorial layout. `study.js` still manages the map and source loading.

Phase 1 changes information architecture only. Existing numerical conclusions are **Needs Review**, explicit modeling inputs are **Assumption**, and missing evidence is **Missing**. No financial audit or data correction is implied. See `docs/phase-1-architecture.md`, `docs/data-review-inventory.csv`, and `docs/research-backlog.md`. `docs/preserved-assets.json` records baseline dataset and model hashes.
