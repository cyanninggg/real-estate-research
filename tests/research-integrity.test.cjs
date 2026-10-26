const fs=require('fs'),path=require('node:path'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),manifest=JSON.parse(fs.readFileSync(path.join(root,'docs/phase-2-preservation.json'),'utf8'));
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
for(const [name,digest]of Object.entries(manifest.assets))assert.equal(hash(fs.readFileSync(path.join(root,name))),digest,'Original research asset changed: '+name);
const source=fs.readFileSync(path.join(root,'index.html'),'utf8');
for(const region of manifest.financial_regions){const start=source.indexOf(region.start),end=source.indexOf(region.end);assert(start>=0&&end>start);assert.equal(hash(source.slice(start,end)),region.sha256,'Financial model or legacy analytical work changed');}
console.log('PASS: original datasets, source records, PDFs, workbook, legacy model functions remain unchanged; the authorized reconciled study update is tested separately.');
assert.equal(hash(fs.readFileSync(path.join(root, "study.js"), "utf8").split("window.CyanStudy=")[0]), "d3c3847c6e73980d47d2945cba85b547c0219f42d5c2c7e6e0455fe3d39de707", "Original map implementation changed");
