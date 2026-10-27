const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),scope={window:{}};
vm.runInNewContext(fs.readFileSync(path.join(root,'reconciled-model.js'),'utf8'),scope);
const content=scope.window.CyanReconciled;
const amount=x=>(x<0?'−':'')+'$'+Math.abs(x).toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});
const includes=(html,x)=>assert(html.includes(amount(x)),`Rendered result missing: ${amount(x)}`);
const close=(a,b)=>assert(Math.abs(a-b)<1e-6,`${a} != ${b}`);
const n=150,rent=3875,vacancy=.05,turnover=.45,eligible=.25,brokerShare=.5,brokerMonths=1;
const mgmt=.03,cap=.052,taxRate=.0124*1.01,opexPerHome=6400,reservePerHome=300;
const cost=9400000+n*640/.85*450*1.25*1.1;
const scenarios=[];
// Independently rebuild both scenarios from the disclosed final workbook inputs.
for(const [market,restricted,voucher] of [[150,0,0],[120,26,4]]){
 const gpr=((market+voucher)*rent+restricted*1440)*12;
 const occupied=market*(1-vacancy),newLeases=occupied*turnover,renewals=occupied*(1-turnover);
 const newFree=newLeases*rent*2,renewalFree=renewals*eligible*rent;
 const egi=gpr*(1-vacancy)-newFree-renewalFree;
 const preTax=egi*(1-mgmt)-n*opexPerHome,value=preTax/(cap+taxRate),tax=value*taxRate,noi=preTax-tax;
 const commission=newLeases*rent*brokerShare*brokerMonths,cash=noi-n*reservePerHome-commission;
 const gap=Math.max(0,cost-value);
 [cost,gpr,-gpr*vacancy,-newFree,-renewalFree,egi,-n*opexPerHome,-egi*mgmt,-tax,noi,-commission,cash,value,gap].forEach(x=>includes(content.results,x));
 assert(content.results.includes((noi/cost*100).toFixed(2)+'%'));
 close(noi/cap,value);
 scenarios.push({egi,preTax,value,tax,noi,newLeases,commission,cash,gap});
}
const base=scenarios[0];
function checkSensitivity(value){includes(content.sensitivity,value*cap);includes(content.sensitivity,value);includes(content.sensitivity,Math.max(0,cost-value));}
for(const change of [-.1,-.05,0,.05,.1])checkSensitivity((base.egi*(1+change)*(1-mgmt)-n*opexPerHome)/(cap+taxRate));
for(const change of [-1000,-500,0,500,1000])checkSensitivity((base.preTax-n*change)/(cap+taxRate));
for(const free of [0,1,2,2.5,3])checkSensitivity(((base.egi-base.newLeases*rent*(free-2))*(1-mgmt)-n*opexPerHome)/(cap+taxRate));
for(const share of [0,.25,.5,.75,1]){includes(content.sensitivity,base.noi);includes(content.sensitivity,base.noi-n*reservePerHome-base.newLeases*rent*share);}
[85274300,1063565.66,1067919.40,4353.74].forEach(x=>includes(content.tax,x));
close(1067919.40-1063565.66,4353.74);
close(85274300*.0124-4353.74+10518.08,1063565.66);
assert(!content.results.includes(amount(1063565.66)));
assert(content.results.includes(content.disclosure));
assert.equal(content.download,'');
const html=Object.values(content).filter(x=>typeof x==='string').join('');
for(const forbidden of ['brokerage','closings','Hew_Public_Data_Underwriting_Reconciled_2026.xlsx','reconciled-model-values.json'])assert(!html.includes(forbidden),`Private payload: ${forbidden}`);
for(const old of ['$3,993,938.97','$3,500,596.39','$76,806,518.58','$11,963,191.64','$13.0M','$433K'])assert(!html.includes(old),`Superseded result: ${old}`);
assert.equal((content.sensitivity.match(/data-reconciled-sensitivity=/g)||[]).length,4);
// Optional local source check; the private workbook export is never copied to the repository.
const privatePath=path.join(root,'../private-model-review/final-workbook-review.json');
if(fs.existsSync(privatePath)){
 const raw=JSON.parse(fs.readFileSync(privatePath));
 const cell=(sheet,ref)=>raw[sheet].find(c=>c.cell===ref).value;
 for(const [i,c]of ['B','C'].entries()){
  const x=scenarios[i];for(const [r,k]of [[25,'egi'],[29,'noi'],[32,'cash'],[35,'value'],[39,'gap']])close(x[k],cell('Pro Forma',c+r));
  close(x.tax,-cell('Pro Forma',c+'28'));close(cost,cell('Pro Forma',c+'17'));
 }
 for(const c of raw.Audit)if(/^B\d+$/.test(c.cell)&&typeof c.value==='number')close(c.value,0);
 for(const r of [5,6,7])for(const c of ['C','F','G'])includes(content.comparables,cell('Market Evidence',c+r));
}
console.log('PASS: both scenarios, all four sensitivities, tax definitions, workbook reconciliation, privacy and superseded-results checks.');
