#!/usr/bin/env python3
"""Real PyQGIS project, projected data, spatial joins and QGIS layout exports."""
import os
os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
from pathlib import Path
import json,csv,hashlib,datetime,math
from qgis.core import *
from qgis.PyQt.QtCore import QVariant,Qt
from qgis.PyQt.QtGui import QColor,QFont,QFontDatabase
ROOT=Path(__file__).resolve().parent
DATA=ROOT/'data';OUT=ROOT/'outputs';OUT.mkdir(exist_ok=True)
app=QgsApplication([],False);app.initQgis()
project=QgsProject.instance();project.setCrs(QgsCoordinateReferenceSystem('EPSG:26986'))
project.setFilePathStorage(Qgis.FilePathType.Relative)
crs=project.crs()
for p in (ROOT/'fonts').glob('*.ttf'):QFontDatabase.addApplicationFont(str(p))
assert 'Source Sans 3' in QFontDatabase().families(), 'Source Sans 3 not loaded'
NAVY='#19364A';TEAL='#4F7F78';INK='#263438';MUTED='#53615e';BG='#FAFAF7'
logs={'qgis_version':Qgis.QGIS_VERSION,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'project_crs':crs.authid(),'distance_units':'meters; projected Cartesian straight-line distances','steps':[],'results':[]}
def load(name):
 l=QgsVectorLayer(str(DATA/(name+'.geojson')),name,'ogr');assert l.isValid(),name;return l
def projected(source,fields=None,clip=None):
 fields=fields or [f.name() for f in source.fields()]
 kind=QgsWkbTypes.displayString(QgsWkbTypes.multiType(source.wkbType()))
 target=QgsVectorLayer(kind+'?crs=EPSG:26986',source.name(),'memory');pr=target.dataProvider();pr.addAttributes([source.fields().field(f) for f in fields]);target.updateFields()
 transform=QgsCoordinateTransform(source.crs(),crs,project);repairs=0;count=0
 for old in source.getFeatures():
  geom=QgsGeometry(old.geometry())
  if geom.isEmpty():continue
  geom.transform(transform)
  if not geom.isGeosValid():geom=geom.makeValid();repairs+=1
  if clip:
   if not geom.intersects(clip):continue
   geom=geom.intersection(clip)
  if geom.isEmpty():continue
  geom.convertToMultiType()
  new=QgsFeature(target.fields());new.setAttributes([old[f] for f in fields]);new.setGeometry(geom);assert pr.addFeatures([new])[0]
  count+=1
 target.updateExtents();logs['steps'].append({'operation':'reproject'+(' and clip' if clip else ''),'source':source.name(),'input_crs':source.crs().authid(),'output_crs':crs.authid(),'input_features':source.featureCount(),'output_features':count,'invalid_geometry_repairs':repairs})
 return target
props=projected(load('properties'))
# A map frame, not an accessibility buffer: cartographic padding around the property extent.
extent=QgsRectangle(props.extent());extent.grow(600)
# Match the print map's 188:142 aspect ratio by widening, without excluding properties.
width=max(extent.width(),extent.height()*188/142);cx=extent.center().x()
extent=QgsRectangle(cx-width/2,extent.yMinimum(),cx+width/2,extent.yMaximum())
clip=QgsGeometry.fromRect(extent)
neighborhoods=projected(load('boston_neighborhoods'),['name','neighborhood_id'],clip)
all_stations=projected(load('massgis_rapid_transit_stations'),['OBJECTID','STATION','LINE','ROUTE'])
stations=projected(load('massgis_rapid_transit_stations'),['OBJECTID','STATION','LINE','ROUTE'],clip)
lines=projected(load('massgis_rapid_transit_lines'),['OBJECTID','LINE','ROUTE'],clip)
roads_source=QgsVectorLayer(str(DATA/'census_roads_2020/tl_2020_25025_roads.shp'),'Census TIGER 2020 Suffolk roads','ogr');assert roads_source.isValid()
roads=projected(roads_source,['LINEARID','FULLNAME','MTFCC'],clip)
water=projected(load('water_context'),['NAME'],clip)
# Spatial point-in-polygon join, then exact planar distance to every official rapid-transit station.
pr=props.dataProvider();pr.addAttributes([QgsField('map_no',QVariant.Int),QgsField('neighborhood',QVariant.String),QgsField('nearest_station',QVariant.String),QgsField('station_id',QVariant.Int),QgsField('distance_m',QVariant.Double),QgsField('station_line',QVariant.String)]);props.updateFields()
for f in props.getFeatures():
 names=[str(n['name']) for n in neighborhoods.getFeatures() if n.geometry().intersects(f.geometry())]
 assert len(names)==1, 'Point neighborhood ambiguous: '+str(f['name'])
 candidates=[(f.geometry().distance(s.geometry()),int(s['OBJECTID']),s) for s in all_stations.getFeatures()]
 dist,_,near=min(candidates,key=lambda v:(v[0],v[1]))
 record={'property_id':str(f['property_id']),'name':str(f['name']),'neighborhood':names[0],'nearest_station':str(near['STATION']),'station_id':int(near['OBJECTID']),'distance_m':dist,'station_line':str(near['LINE'])}
 logs['results'].append(record)
 changes={'map_no':{'hew':1,'harper':2,'alder':3}[str(f['property_id'])],'neighborhood':names[0],'nearest_station':record['nearest_station'],'station_id':record['station_id'],'distance_m':dist,'station_line':record['station_line']}
 pr.changeAttributeValues({f.id():{props.fields().indexFromName(k):v for k,v in changes.items()}})
logs['steps'] += [{'operation':'point-in-polygon spatial join','predicate':'intersects; exactly one neighborhood required'}, {'operation':'nearest station','method':'minimum QgsGeometry.distance across all 170 official station features in EPSG:26986','not':'walking/network distance, station entrance distance, or travel time'}]
# Save all editable presentation and analysis layers in a genuine GeoPackage.
gpkg=ROOT/'hew_comparables.gpkg'
if gpkg.exists():gpkg.unlink()
def persist(layer,name,first=False):
 opt=QgsVectorFileWriter.SaveVectorOptions();opt.driverName='GPKG';opt.layerName=name;opt.fileEncoding='UTF-8';opt.actionOnExistingFile=QgsVectorFileWriter.CreateOrOverwriteFile if first else QgsVectorFileWriter.CreateOrOverwriteLayer
 result=QgsVectorFileWriter.writeAsVectorFormatV3(layer,str(gpkg),project.transformContext(),opt);assert result[0]==QgsVectorFileWriter.NoError,(name,result)
 out=QgsVectorLayer(str(gpkg)+'|layername='+name,name,'ogr');assert out.isValid();project.addMapLayer(out);return out
props=persist(props,'Property locations and spatial results',True)
neighborhoods=persist(neighborhoods,'Boston neighborhood boundaries')
roads=persist(roads,'Census road context')
water=persist(water,'Major water features')
lines=persist(lines,'MassGIS rapid transit lines')
stations=persist(stations,'MassGIS rapid transit stations')
# Styling uses QGIS renderers, not manually drawn SVG marker positions.
nsymbol=QgsFillSymbol.createSimple({'color':'239,241,233,255','outline_color':'171,185,175,255','outline_width':'0.25','outline_style':'dash'})
neighborhoods.renderer().setSymbol(nsymbol)
roads.renderer().setSymbol(QgsLineSymbol.createSimple({'line_color':'205,211,204,255','line_width':'0.35','line_width_unit':'MM'}))
water.renderer().setSymbol(QgsFillSymbol.createSimple({'color':'216,230,230,255','outline_style':'no'}))
lines.renderer().setSymbol(QgsLineSymbol.createSimple({'line_color':TEAL,'line_width':'0.85','line_width_unit':'MM'}))
stations.renderer().setSymbol(QgsMarkerSymbol.createSimple({'name':'circle','color':'255,255,255,255','outline_color':TEAL,'outline_width':'0.65','size':'2.1'}))
categories=[]
for key,label,color,shape,size in [('hew','Subject property',NAVY,'diamond','4.8'),('harper','Rental comparable',TEAL,'circle','3.8'),('alder','Rental comparable',TEAL,'circle','3.8')]:
 sym=QgsMarkerSymbol.createSimple({'name':shape,'color':color,'outline_color':'255,255,255,255','outline_width':'.65','size':size});categories.append(QgsRendererCategory(key,sym,label))
props.setRenderer(QgsCategorizedSymbolRenderer('property_id',categories))
def labels(layer,field,size,color,placement=Qgis.LabelPlacement.AroundPoint,expression=False):
 s=QgsPalLayerSettings();s.fieldName=field;s.isExpression=expression;s.placement=placement;s.dist=2.8;s.priority=8
 fmt=QgsTextFormat();fmt.setFont(QFont('Source Sans 3',size));fmt.setSize(size);fmt.setColor(QColor(color))
 buf=QgsTextBufferSettings();buf.setEnabled(True);buf.setSize(.9);buf.setColor(QColor(BG));fmt.setBuffer(buf);s.setFormat(fmt)
 layer.setLabeling(QgsVectorLayerSimpleLabeling(s));layer.setLabelsEnabled(True)
labels(props,'lpad(to_string("map_no"),2,\'0\') || \'  \' || "name"',12,NAVY,expression=True)
# Label only major local road names; every line remains available in the editable dataset.
labels(roads,'CASE WHEN "FULLNAME" IN (\'Commonwealth Ave\',\'Brighton Ave\',\'Cambridge St\',\'Market St\',\'Guest St\',\'Western Ave\') THEN "FULLNAME" END',10,MUTED,Qgis.LabelPlacement.Line,True)
labels(stations,'CASE WHEN "OBJECTID" IN (135,138) THEN "STATION" END',11,TEAL,expression=True)
# No institution names are introduced as map annotations.
# Use two unobtrusive layout labels for neighborhood names, tied to polygon geometry via QGIS labeling.
labels(neighborhoods,'upper("name")',13,'#83928c',Qgis.LabelPlacement.Horizontal,True)
map_layers=[props,stations,lines,roads,water,neighborhoods]
project.layerTreeRoot().setHasCustomLayerOrder(True);project.layerTreeRoot().setCustomLayerOrder(map_layers)
project.viewSettings().setDefaultViewExtent(QgsReferencedRectangle(extent,crs))
layout=QgsPrintLayout(project);layout.initializeDefaults();layout.setName('Hew rental comparable geographic analysis');layout.pageCollection().pages()[0].setPageSize('A4',QgsLayoutItemPage.Landscape)
layout.renderContext().setDpi(300)
def text(value,x,y,w,h,size=11,color=INK,bold=False):
 item=QgsLayoutItemLabel(layout);item.setText(value);font=QFont('Source Sans 3');font.setPointSizeF(float(size));font.setBold(bold);item.setFont(font);item.setFontColor(QColor(color));item.setMargin(0);layout.addLayoutItem(item);item.attemptMove(QgsLayoutPoint(x,y));item.attemptResize(QgsLayoutSize(w,h));return item
text('RENTAL MARKET / GIS EXHIBIT',12,7,270,6,10,TEAL,True)
text('Hew and Its Rental Comparables',12,15,275,12,23,NAVY,True)
text('Allston–Brighton, Boston  |  Property locations, neighborhoods and rapid-transit context',12,29,274,7,11,MUTED)
map_item=QgsLayoutItemMap(layout);layout.addLayoutItem(map_item);map_item.attemptMove(QgsLayoutPoint(12,42));map_item.attemptResize(QgsLayoutSize(188,142));map_item.setLayers([]);map_item.setKeepLayerSet(False);map_item.zoomToExtent(extent);map_item.setBackgroundColor(QColor(BG));map_item.setFrameEnabled(True);map_item.setFrameStrokeColor(QColor('#ccd4cb'));map_item.setFrameStrokeWidth(QgsLayoutMeasurement(.25));map_item.setId('Main geographic map')
# Sidebar results are editable layout text. Distances come from the spatial calculations above.
for i,record in enumerate(sorted(logs['results'],key=lambda r:{'hew':0,'harper':1,'alder':2}[r['property_id']])):
 y=43+i*37
 role='SUBJECT PROPERTY' if i==0 else 'RENTAL COMPARABLE'
 text(f'{i+1:02d} / {role}',209,y,76,6,9.5,TEAL,True)
 text(record['name'],209,y+7,76,8,13,NAVY,True)
 text(record['neighborhood']+' neighborhood',209,y+16,76,7,11,MUTED)
 text(f'Nearest rapid transit: {record["distance_m"]:.0f} m',209,y+24,76,7,11,INK)
text('Projected straight-line distance to a station point.\nNot a walking route or station entrance measure.',209,157,76,15,9.5,MUTED)
text('◆  Subject',209,176,34,7,10.5,NAVY)
text('●  Comparable',245,176,42,7,10.5,TEAL)
text('○  Rapid-transit stop    ━  Rapid-transit line',12,187,190,7,10.5,TEAL)
# True scale bar linked to the QGIS map CRS, not a manually drawn distance annotation.
scale=QgsLayoutItemScaleBar(layout);scale.setStyle('Single Box');scale.setLinkedMap(map_item);scale.setUnits(Qgis.DistanceUnit.Meters);scale.setUnitsPerSegment(250);scale.setNumberOfSegments(2);scale.setNumberOfSegmentsLeft(0);scale.setUnitLabel('m');scale.setFont(QFont('Source Sans 3',9));scale.setHeight(1.5);scale.setBackgroundEnabled(True);scale.setBackgroundColor(QColor(BG));layout.addLayoutItem(scale);scale.attemptMove(QgsLayoutPoint(16,173));scale.applyDefaultSize();scale.setUnitsPerSegment(250);scale.setNumberOfSegments(2);scale.setNumberOfSegmentsLeft(0)
# North is grid north in the projected CRS; map rotation remains zero.
text('↑ N',185,46,12,12,16,NAVY,True)
text('Sources: Boston Planning Department; MassGIS / CTPS / MBTA; Census roads and geocoding; official property map.',12,196,273,5,8.5,MUTED)
text('EPSG:26986 · NAD83 / Massachusetts Mainland (meters) · Prepared 27 October 2026 in QGIS '+Qgis.QGIS_VERSION.split('-')[0],12,201,273,5,8.5,MUTED)
project.layoutManager().addLayout(layout)
project.setTitle('Hew at 1515 — Rental Comparable Geographic Analysis')
assert project.write(str(ROOT/'hew_rental_comparables.qgz'))
exporter=QgsLayoutExporter(layout)
svg=QgsLayoutExporter.SvgExportSettings();svg.dpi=300;svg.forceVectorOutput=True;svg.exportAsLayers=True;svg.textRenderFormat=Qgis.TextRenderFormat.AlwaysOutlines
pdf=QgsLayoutExporter.PdfExportSettings();pdf.dpi=300;pdf.forceVectorOutput=True;pdf.textRenderFormat=Qgis.TextRenderFormat.AlwaysText
assert exporter.exportToSvg(str(OUT/'hew-rental-comparables.svg'),svg)==QgsLayoutExporter.Success
assert exporter.exportToPdf(str(OUT/'hew-rental-comparables.pdf'),pdf)==QgsLayoutExporter.Success

logs['map_extent_26986']={'xmin':extent.xMinimum(),'ymin':extent.yMinimum(),'xmax':extent.xMaximum(),'ymax':extent.yMaximum(),'method':'600m cartographic padding around property bounding box, aspect-ratio adjusted; not a catchment or accessibility buffer'}
logs['project']='hew_rental_comparables.qgz';logs['geopackage']='hew_comparables.gpkg';logs['layout']=layout.name();logs['exports']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.suffix in ['.pdf','.svg']}
(ROOT/'qgis_processing_log.json').write_text(json.dumps(logs,indent=2)+'\n')
with (ROOT/'spatial_results.csv').open('w',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=list(logs['results'][0]),lineterminator='\n');writer.writeheader();writer.writerows(logs['results'])
print(json.dumps({'version':Qgis.QGIS_VERSION,'spatial_results':logs['results'],'exports':list(logs['exports'])},indent=2))
# Avoid provider teardown races during interpreter shutdown; resources are flushed above.
