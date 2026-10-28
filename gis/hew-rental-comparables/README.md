# Hew rental comparables — QGIS geographic analysis

Produced on 27 October 2026 with **QGIS / PyQGIS 3.44.15**. This is an editable QGIS project and native QGIS Print Layout export, not a hand-positioned SVG or screenshot of a web map.

## Deliverables

- `hew_rental_comparables.qgz`: genuine QGIS project containing one editable A4 landscape Print Layout.
- `hew_comparables.gpkg`: six projected, editable GIS layers: three property locations/spatial results, two neighborhood polygons, 501 clipped road features, one water feature, two rapid-transit line features and seven station points. These are clipped feature counts, not citywide inventory or measures of access.
- `outputs/hew-rental-comparables.svg`: vector web exhibit; QGIS-generated text outlines preserve Source Sans 3.
- `outputs/hew-rental-comparables.pdf`: vector PDF with readable text for portfolio/presentation use.
- `build_qgis.py`: actual executed PyQGIS processing, styling and layout-export code.
- `prepare_data.py`, `download_context.py`: reproducible source download/preparation scripts.
- `spatial_results.csv`, `qgis_processing_log.json`, `project_validation.json`: computed results, processing parameters and validation records.
- `source_manifest.json`, `context_sources.json`, `property_source_register.json`: data provenance and source/version records.

The download package includes the project, GeoPackage, exports, code, font files and source records. It opens offline with the `.qgz` beside the `.gpkg`. Complete original regional input downloads can be recreated with the source scripts; they are not duplicated in the public package.

## Sources and location validation

1. **Property points:** the existing geographic source register. Hew and Harper were rechecked against the U.S. Census Geocoder on 27 October 2026 and matched the stored coordinates. Alder uses the named property place reached from the official property's published map link. These are approximate address/property locations, not surveyed building entrances.
   - [Census Geocoder](https://geocoding.geo.census.gov/geocoder/)
   - [Alder official website](https://www.livealder.com/) / [published property map](https://maps.app.goo.gl/YEQpbjmF7fcBPNKMA)
2. **Boston neighborhoods:** [official Planning Department layer](https://gis.bostonplans.org/hosting/rest/services/Hosted/Boston_Neighborhood_Boundaries/FeatureServer/5), copyright BPDA / Planning Department. All 26 features were retrieved before clipping.
3. **Rapid transit:** [MassGIS metadata](https://www.mass.gov/info-details/massgis-data-mbta-rapid-transit), [detailed station layer](https://arcgisserver.digital.mass.gov/arcgisserver/rest/services/AGOL/MBTA_Rapid_Transit/MapServer/3) and [detailed line layer](https://arcgisserver.digital.mass.gov/arcgisserver/rest/services/AGOL/MBTA_Rapid_Transit/MapServer/4). Credits: MBTA, CTPS, MassGIS. Source counts: 170 station features and 141 line features. Rapid transit does **not** include commuter rail or all bus services.
4. **Road context:** [U.S. Census Bureau TIGER/Line 2020 Suffolk County roads](https://www2.census.gov/geo/tiger/TIGER2020/ROADS/tl_2020_25025_roads.zip). Historical cartographic context, not a current engineering road inventory. Inconsistent geometry returned by a separate road-service query was rejected rather than used.
5. **Water context:** [MassGIS Major Hydrography](https://arcgisserver.digital.mass.gov/arcgisserver/rest/services/AGOL/Hydro_Major/MapServer/2).

Exact download requests, retrieval timestamps and input-response SHA-256 hashes are retained in the source records. New downloads may reflect revised public services; compare hashes before claiming an exact historical reproduction.

## Coordinate systems and processing

- Input property/GeoJSON coordinates use longitude, latitude (WGS84 / EPSG:4326).
- Boston's native service CRS is EPSG:2249, Massachusetts Mainland in US survey feet. MassGIS transit's native CRS is EPSG:26986, Massachusetts Mainland in meters. GeoJSON requests explicitly requested WGS84 output; these source CRS distinctions were retained.
- PyQGIS genuinely reprojected each input to **EPSG:26986 (NAD83 / Massachusetts Mainland, meters)** using `QgsCoordinateTransform`. It did not merely relabel coordinates.
- Source geometries were checked; `makeValid()` was applied where needed, with counts recorded. Context layers were intersected with the print map extent. Source length/area attributes were not treated as newly measured values.
- The map extent uses 600 meters of cartographic padding around the property bounding box, widened to the map frame aspect ratio. This is a layout choice, not an accessibility buffer.
- A point-in-polygon spatial join assigned the official neighborhood to each property point. A unique match was required.
- `QgsGeometry.distance` measured projected straight-line distance from each property point to **every one of the 170 rapid-transit station points**. The minimum was retained. This is not network routing, travel time, station-entrance distance or a pedestrian-access claim.

| Property | Official neighborhood at point | Nearest rapid-transit station point | Projected straight-line distance |
|---|---|---|---:|
| Hew at 1515 | Brighton | Warren Street | 184 m |
| Harper | Allston | Harvard Avenue | 709 m |
| Alder at Allston Yards | Brighton | Warren Street | 806 m |

Displayed distances are rounded to whole meters; unrounded outputs are retained in the GeoPackage and CSV. The neighborhood assignment follows the official polygon at the approximate point, not a property's marketing neighborhood. No rent premium, travel-time estimate or causal transit effect was calculated.

## Cartographic production

Native QGIS renderers distinguish the navy diamond subject and teal circle comparables. The layout includes official neighborhood boundaries, street context, transit infrastructure, GIS-controlled labels, a map-linked scale bar, grid-north annotation, source credits and CRS/date notes. Source Sans 3 is included under its SIL Open Font License. Make the bundled fonts available in QGIS when editing the layout; the web SVG uses outlines and the exported PDF embeds its text fonts. SVG and PDF were exported through `QgsLayoutExporter` from the saved Print Layout.

## Reproduce

1. Install/use a genuine QGIS distribution with PyQGIS. The production run used the QGIS app already present on the user's desktop; no software was installed by the workflow.
2. Open `hew_rental_comparables.qgz` with `hew_comparables.gpkg` beside it to inspect and edit the existing layers/layout offline.
3. To rebuild from source downloads, run `python3 prepare_data.py` then `python3 download_context.py` in this package directory (internet required). Source timestamps/hashes can change as services are updated.
4. Run the project builder with QGIS's bundled Python, for example:

```sh
QT_QPA_PLATFORM=offscreen "$QGIS_APP/Contents/MacOS/python" build_qgis.py
```

Set `QGIS_APP` to the installed QGIS app location. This is the application path, not an instruction to install or alter it. The script saves the editable project/GeoPackage and exports SVG/PDF. It reads bundled fonts from `fonts/`.

## Validation and limits

The saved project was copied with its GeoPackage to another directory and reopened in real PyQGIS. All six layers loaded in EPSG:26986, all saved geometries passed QGIS validity checking, and the editable Print Layout remained present. The project contains relative data paths and no local user-directory paths. The PDF was independently rendered with Poppler and visually inspected for labels, clipping, legend and scale.

This analysis demonstrates source handling, location validation, CRS transformation, spatial joining, nearest-feature measurement and QGIS layout production. It does not establish surveyed positions, pedestrian accessibility, transit service frequency, realized rents, building-level performance or an investment conclusion. Financial results and the rest of the portfolio were not changed.

### Final release clarification

Alder’s official address is **301 Guest Street, Boston, MA 02134**. Its official website names the development **Allston Yards**; the validated property point intersects the Planning Department’s **Brighton** polygon. Public presentation therefore uses “Brighton · Allston Yards development.” This preserves the computed official-boundary result and distinguishes it from the development’s marketed name; it is not an address or point correction.

**Boston Landing is commuter rail**, on the Framingham/Worcester Line ([Boston Landing’s station information](https://www.bostonlanding.co/places/commuter-rail)). It is outside the MassGIS rapid-transit layer used here. Alder’s 806 m result is the nearest *rapid-transit station point*, not the nearest station of any type. No commuter-rail distance or walking-access measure has been calculated. The map, project, coordinates and spatial results are unchanged.
