# Phase 1 — Structure and research status

## Audit

The site is buildless HTML/CSS/JavaScript. `index.html` owns hash routing, legacy page constructors, shared comparison data, the Hew operating/development model, chart rendering, CSV export and Everett lease calculator. `study.js` owns the Brighton report, Leaflet lifecycle, CSV loading, popups and mapping. `study.css` scopes the report presentation. The site is served from the root of `main` by GitHub Pages; no package install or framework migration is needed.

The local export matched the three source files on main at the start. The containing workspace has unrelated untracked files; they were preserved. Reusable foundations include model controls, comparison tables, summary objects, report data, map lifecycle, responsive wrappers and existing downloads. Problems: homepage counted only two cases; nav exposed case names rather than a hierarchy; methodology mixed source definitions and model assumptions; narrative order differed by case; model findings were prominent without an explicit review status.

## Revised hierarchy and route mapping

| Existing route | Revised role | URL |
| --- | --- | --- |
| `#/` | Home / Research Portfolio; three selected studies, Brighton first | unchanged |
| Individual case links in global navigation | Research index | `#/research` |
| `#/study` | Case 01 — Development Feasibility & Housing Policy | unchanged |
| `#/b/hew/overview` | Case 02 — Residential Market & Asset Analysis | unchanged |
| `#/b/everett/overview` | Case 03 — Large-Scale Urban Development | unchanged |
| `#/b/{case}/{renter,asset,development,compare}` | Selected legacy analysis inside the shared case narrative | unchanged |
| `#/b/harper/*` | Harper remains the Hew pricing comparison | existing redirect preserved |
| `#/method` | Research methodology, status definitions, retained source record | unchanged |
| About section formerly on home | About / Resume; existing biography and contact links | `#/about` |
| `resume.pdf`, existing data/PDF/model downloads | Supporting materials | unchanged |
| `brighton-development-feasibility.html` | Compatibility redirect to the merged study | unchanged |

The shared `CyanPortfolio` template renders question, framework, evidence, analysis, findings, implications and sources. Legacy analysis subroutes select one original tool/panel and land at the Analysis section. The surrounding narrative remains available above and below. Case 01 preserves its demographic tables, map, pro forma, charts, policy scenario and workbook download. Case 02 and Case 01 explicitly retain different assumptions.

## Integrity boundaries

No financial formulas, datasets, workbook values or source files are corrected in Phase 1. `preserved-assets.json` records starting hashes for all JSON/CSV/XLSX/PDF research assets. `data-review-inventory.csv` captures existing numeric paragraphs/table rows, model input conventions, existing result summaries, high-priority issues and authoring backlog. It is a review queue, not verification evidence. All existing numerical conclusions are Needs Review; explicit input conventions are Assumption; missing citations/tasks are Missing. Nothing is automatically Verified.

The inventory preserves original statements, including potentially incorrect or conflicting claims. The public status notice qualifies existing analysis. The old source record is retained, but prior language such as “checked” does not override the new review classification. Source presence is not proof of validity. Missing-data placeholders in the report now read as an evidence limitation; internal author instructions are retained in the inventory rather than public copy.

## Phase 2 priorities

Trace the Hew unit schedule, NOI, concessions, tax convention and valuation; audit construction/land cost scope; review inclusionary rules, affordable rents and AMI; test tax-abatement duration and capitalization; reconcile Everett cost scope and listing dates; complete item-level citations. Do not silently reconcile the two Hew scenarios. Infrastructure finance, interviews, stakeholder engagement and econometrics are not claimed as completed research.

## Deployment

Normal repository workflow publishes pushes to main through branch-based GitHub Pages. No new deployment system or dependency is added. Retain this document and the review inventory as repository documentation, outside the primary site navigation.
