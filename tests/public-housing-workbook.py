"""Read-only validation of the final supplied public workbook; never recalculates or edits it."""
import json,sys,zipfile,xml.etree.ElementTree as E
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'data/Hew_Underwriting_Public_Edition_2026.xlsx'
ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(p) as z:
 assert z.testzip() is None
 wb=E.fromstring(z.read('xl/workbook.xml'));rels={r.attrib['Id']:r.attrib['Target'] for r in E.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
 strings=[]
 if 'xl/sharedStrings.xml' in z.namelist():strings=[''.join(x.itertext()) for x in E.fromstring(z.read('xl/sharedStrings.xml'))]
 sheets={};formulas=0
 for sh in wb.find('s:sheets',ns):
  t=rels[sh.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']];t=t.lstrip('/') if t.startswith('/') else 'xl/'+t;cells={}
  for c in E.fromstring(z.read(t)).findall('.//s:sheetData/s:row/s:c',ns):
   assert c.attrib.get('t')!='e','Cached Excel error'
   v=c.find('s:v',ns);f=c.find('s:f',ns);text=v.text if v is not None else ''.join(c.find('s:is',ns).itertext()) if c.find('s:is',ns) is not None else ''
   if c.attrib.get('t')=='s':text=strings[int(text)]
   if f is not None:formulas+=1;assert text is not None and text!='','Missing formula cache'
   cells[c.attrib['r']]=text
  sheets[sh.attrib['name']]=cells
 assert len(sheets)==11 and 'Affordable Housing' in sheets
 assert sheets['Affordable Housing']['B21']=='2'
 assert all(not sheets['Audit'].get(c) for c in ['A30','A31'])
 assert all(float(sheets['Audit'][f'B{r}'])==0 for r in range(38,51))
 for c,v in {'B31':48,'B32':67,'B33':35,'C34':26,'D34':5,'E34':119,'I34':456192,'O34':168456}.items():assert float(sheets['Affordable Housing'][c])==v
 assert formulas>0
 print(json.dumps({'housing':{c:float(sheets['Affordable Housing'][c]) for c in ['B21','B34','C34','D34','E34','F40','F41']},'proforma':{c:float(sheets['Pro Forma'][c]) for c in ['B17','B25','B29','B32','B35','B39','C17','C20','C25','C28','C29','C32','C35','C36','C39','C40']},'formulaCells':formulas,'housingAudits':13}))
