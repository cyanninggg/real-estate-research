# Phase 2 — Research presentation and Analyst Learning Lab

## Scope and audit

This phase follows the supplied Phase 2 brief, which explicitly defers financial data auditing. It supersedes the earlier Phase 1 document's suggestion that the next phase would audit figures. No financial inputs, outputs, formulas or source datasets were corrected. The existing buildless HTML/CSS/JavaScript and hash router remain in place. No backend, authentication or framework was introduced.

The initial source consists of `index.html` (router, financial tools and original analytical pages), `study.js` (supplied Brighton report and source-aware Leaflet map), `portfolio.js` (shared presentation) and scoped CSS. Existing datasets, workbook, PDFs and the original review inventory were preserved. Unrelated untracked workspace files were not overwritten. The report text and model constructors remain available even where presentation components qualify headings or reorganize the narrative.

## Reference review

The actual supplied **Downtown Office Conversion Study — Summary Report, July 2023**, prepared by HR&A Advisors for BPDA with project partners, was read and visually inspected before implementation. It is 30 pages. All pages were rendered for visual review; alternative comparison, sensitivity and recommendation pages were inspected at larger size. The supplied copies had matching SHA-1 `98b5652610a6885bd7b2be094eaf7a4c8a377a86`.

Transferable principles and original adaptation:

- PDF pp. 6–15: a scoped market question, a main takeaway, supporting comparisons and sources. The portfolio now pairs topic labels with cautious analytical headlines.
- PDF pp. 21–23: explain drivers and compare alternatives rather than isolate outputs. Original issue trees and decision contexts frame the unchanged model scenarios.
- PDF pp. 26–29: distinguish mechanisms, fiscal effects and implementation. The original policy-options component records objectives, feasibility effects, fiscal implications, eligibility and evidence gates.
- Existing Cyan Li green / neutral identity is retained. No report photographs, maps, graphics, logos, distinctive slide layouts or branded palette were copied.

The report concerns historical Downtown office conversions. Brighton is a hypothetical ground-up project. No report costs, typologies, rents, affordability rules, subsidy levels, abatement periods or financial outcomes were imported. `#/lab/reference` explains this distinction with page references and a link to the official resource page. The full copyrighted reference PDF was not added to the public repository.

## Public portfolio

Global navigation remains Home, Research, Methodology, About / Resume. A small homepage / footer link opens the Lab. Existing routes remain valid.

The reusable report shell now has eight sections: executive summary; decision context; framework and hypotheses; evidence; financial/economic analysis; findings; preliminary implications and next steps; limitations and sources. Each case names the decision-maker, stakeholders, alternatives, constraints and success criteria. Assertion-led headings remain conditional where evidence is provisional. Issue trees describe analytical dependencies, not proven causal relationships. Action notes name the actor, proposed next step, rationale, expected effect / trade-off and verification gate.

Desktop contents remain visible while reading. Mobile has a labeled section selector. Wide evidence tables retain local scrolling; the main Brighton scenario table fits the mobile viewport. Existing charts, accessible exact-value tables, map controls, input sliders, reset, CSV export, concession calculator and downloads are preserved.

## Learning Lab architecture

`#/lab` provides Learn → Practice → Research → Validate → Publish → Reflect. Publication is a separate reviewed action; there is no auto-publish feature.

| Area | Routes / implementation |
| --- | --- |
| Consulting Toolkit | `#/lab/toolkit`, `#/lab/lesson/{id}`. Three authored foundational lessons: MECE, Issue Trees, Hypothesis-driven Thinking. Five additional frameworks are explicitly labeled outlines. |
| Technical Skills | `#/lab/skills`, `#/lab/skill/{id}`. Four skill categories, learning/practice/application links and evidence-based self-assessment. |
| Case Practice | `#/lab/practice`, `#/lab/case/{id}`. Residential market sizing, affordable development feasibility, office conversion. Qualitative exercises without fabricated numerical answers. |
| Research & Data Review | `#/lab/review`, `sources`, `assumptions`, `dependencies`, `hypotheses`, `questions`, `revisions`. Read-only original inventory plus local review notes, filters and research plans. |
| Career Preparation | `#/lab/career`. Job-to-skill mapping, technical answers, real behavioral-story template and portfolio presentation prompts. |
| Progress | `#/lab/progress`. Self-assessed stages, evidence, reflection and JSON transfer. |
| Reference methods | `#/lab/reference`. Attribution and the boundary between the historical reference and Brighton. |

Career mapping uses the complete Analyst, Real Estate JD supplied by the user, including econometrics, infrastructure finance, fiscal/economic impact, GIS, client documents and responsible AI verification. The source URL and publication date were not supplied; current vacancy status is not asserted. It does not invent experience, credentials or completed econometric / infrastructure work. Degree-only, school-name-free application preparation is noted.

## Persistence and separation

Public GitHub Pages routes and authored lesson materials are publicly accessible; the Lab is not an authenticated private area. User entries use browser-local storage under `cyan-research-lab-v1`; they are not uploaded or synced. Clearing browser storage may remove them. No sensitive information should be entered. Export/import transfers a versioned JSON workspace, not source datasets.

Separate stores contain notes, competency evidence, hypothesis assessments, local review overrides, research plans and revision notes. Data statuses and hypothesis statuses are independent. No result is automatically Verified and no competency advances on visiting a lesson. Selecting independently applied requires evidence; selecting Verified requires a review note. These are user records, not certification or publication. Original CSV records and public case status remain unchanged.

Import validates version, identifiers, enumerations and text bounds, rejects prototype-related keys and unsupported records, and asks before replacing local Lab entries. User text is escaped on rendering. The interface supports a current-session fallback when browser storage is unavailable.

## Major changed files

- `index.html`: Lab route lifecycle and new module links; original model functions unchanged.
- `portfolio.js`: eight-section shell, summaries, sticky/mobile contents, conditional presentation and Lab links.
- `research-components.js`: original executive summary, decision context, issue tree, policy options, next-step and learning-link components.
- `lab-content.js`: structured lessons, skill tasks, practice cases, hypotheses, questions and supplied-JD mapping.
- `lab.js`: routes, local storage, import/export, filtering, review editors and validation.
- `lab.css`: original research / workspace presentation and responsive treatment.
- README, preservation manifest and tests: maintenance / validation documentation.

## Known limits and next steps

This is not a financial or policy audit. Existing numerical conclusions remain Needs Review. Source gaps, operating records and conflicting assumptions still require a separately authorized audit. Five framework lessons are outlines; technical skill pages provide architecture and tasks rather than a complete training curriculum. Practice cases are qualitative because no new validated exercise inputs were supplied. No live Excel editor, scored assessment, econometric engine, account system, private server or cross-device sync is included. The official resource-page link does not verify current program rules. Mapping continues to depend on external Leaflet / OpenStreetMap services.

Next: use the Lab to record a real exercise and its evidence, expand a specific outline when needed, and plan a separately scoped source/model audit before upgrading public conclusions or recommending policy action.
