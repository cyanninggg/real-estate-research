const fs=require('fs'),path=require('node:path'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),manifest=JSON.parse(fs.readFileSync(path.join(root,'docs/phase-2-preservation.json'),'utf8'));
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
for(const [name,digest]of Object.entries(manifest.assets))assert.equal(hash(fs.readFileSync(path.join(root,name))),digest,'Original research asset changed: '+name);
const source=fs.readFileSync(path.join(root,'index.html'),'utf8');
for(const region of manifest.financial_regions){const start=source.indexOf(region.start),end=source.indexOf(region.end);assert(start>=0&&end>start);assert.equal(hash(source.slice(start,end)),region.sha256,'Financial model or legacy analytical work changed');}
assert.equal(hash(fs.readFileSync(path.join(root,'study.js'))),manifest.study_js_sha256,'Supplied study or map implementation changed');
console.log('PASS: original datasets, source records, PDFs, workbook, model functions and supplied study remain unchanged.');
