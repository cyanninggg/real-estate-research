# Phase 2 validation

## Checks actually run

- JavaScript syntax checks for the inline application and all new / changed script modules.
- `node tests/lab-state.test.cjs`: versioned state validation, enum / identifier validation, empty-evidence guardrails, prototype-key rejection, escaped user text, quoted/newline CSV parsing, inventory loading, authored lesson count and Lab route rendering.
- `node tests/research-integrity.test.cjs`: original CSV/JSON/PDF/XLSX assets, original financial constants / model and legacy analysis functions, and supplied Brighton report/map implementation remain unchanged.
- Browser checks of 41 public / Lab / lesson / practice routes, plus 28 technical-skill routes: expected headings / forms, eight sections per research case, no empty pages or duplicate element IDs.
- Desktop sticky contents and mobile labeled section menu; selected analysis section aligned below the mobile contents control.
- Mobile viewport 390 × 844: page width matched viewport width. Main Brighton scenario table readable side by side; wide inventory / evidence tables scroll within their containers.
- Existing Leaflet map loaded sourced markers. Keyboard activation of the Hew marker opened the unit / rent / concession popup. Unknown rents remain unavailable.
- Existing Hew turnover input changed the displayed scenario; reset restored its starting value. Existing Everett selector retained Anthem's half-month broker assumption and note. No calculation accuracy is claimed by these UI tests.
- Original resume, Census PDF, full Excel model, listing JSON and review CSV served successfully from local preview and matched original bytes.
- Learning notes and hypothesis assessment persisted through reload. Combined inventory search / case / priority filters and question topic filter worked. Invalid Verified / Independently Applied selections without evidence were rejected.
- JSON progress export produced the expected local notes, hypothesis, review and competency fields. Invalid version import was rejected. Valid import required confirmation and restored progress. An empty import removed QA entries; no QA competency or note was retained as the user's work.
- The suggested-method disclosure opened in the office-conversion practice case. Browser console error inspection after map / report checks returned no errors.
- University-name scan of new authored website files passed. No reference-report visual assets were added.

## Boundaries

These checks validate presentation and workflow, not the accuracy of financial, market, demographic or policy data. Existing findings remain Needs Review. The complete historical reference was read and visually inspected, but no historical parameters were adopted as current Brighton facts. The supplied JD informs career preparation; the posting URL / date and current opening status are not verified.

No package build exists: GitHub Pages serves static files. Existing normal branch-based deployment is retained. Browser-local persistence depends on the user's browser and origin; it does not provide authentication, private server storage or synchronization. External map services remain a dependency.
