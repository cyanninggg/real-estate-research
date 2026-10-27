/* One research report for the existing study and Hew routes. */
(function(){'use strict';
var question='How do leasing concessions, operating-cost assumptions, and publicly documented property taxes affect the underwriting of newly developed multifamily housing in Brighton, Boston?';
var sections=[['question','The Question'],['framework','Analytical Framework'],['evidence','Evidence & Research'],['analysis','Financial & Economic Analysis'],['findings','Key Findings & Recommendations'],['sources','Limitations & Sources']];
var scrollHandler=null;
function destroy(){if(scrollHandler)window.removeEventListener('scroll',scrollHandler);scrollHandler=null;}
function section(id,title,body,index){return '<section class="case-section" id="case-'+id+'"><div class="wrap"><div class="section-kicker">'+String(index+1).padStart(2,'0')+' / '+title.toUpperCase()+'</div>'+body+'</div></section>';}
function context(){
 var t=document.createElement('template');t.innerHTML=window.CyanStudy.html;
 var market=t.content.querySelector('#study-market > .wrap');
 var html=market.innerHTML, end=html.indexOf('<h3>Hew’s advertised rents');
 if(end>=0)html=html.slice(0,end);
 html=html.replace(/<div class="section-kicker">[\s\S]*?<\/div>/,'').replace(/<h2>[\s\S]*?<\/h2>/,'<h3>Regional demographic and spatial context</h3>');
 return '<details id="hew-context"><summary>Explore regional demographics and the site map</summary><p>Context only: regional demographics and proximity do not establish Hew’s absorption, turnover or achieved rent.</p>'+html+'</details>';
}
function history(){
 return '<details><summary>Earlier samples: October 18 comparison and October 19 Harper listings</summary><p>The dated samples below are retained as historical evidence. They are separate from the revised financial model and do not establish actual occupancy. Figures are rounded in the original comparison.</p>'+window.CyanHew.historyHTML+'</details>';
}
function render(){var m=window.CyanReconciled;
 var process=['Market Evidence','Effective Rent','Operating Assumptions','NOI Illustration','Sensitivity Analysis','Findings and Recommendations'];
 var bodies=[
 '<h2 class="case-section-title">What does an advertised rent leave out?</h2><p class="lead">'+question+'</p><p>Hew at 1515 is a 150-home rental community in Brighton, marketed at 1525 Commonwealth Avenue. The Allston–Brighton market includes newer competing apartment buildings. Harper and Alder provide selected rent comparisons; differences in unit size, lease date and incentives matter.</p><p>This study follows the income an owner could retain after free rent, collection loss, operating costs and property tax. It combines dated market observations with municipal records, then demonstrates the calculations in a separate hypothetical development model.</p><p class="report-source">Property facts: <a href="https://livehew.com/faqs/" target="_blank" rel="noopener">Hew official FAQ ↗</a>, checked 26 October 2026. Study cutoff: 26 October 2026.</p>',
 '<h2 class="case-section-title">From market evidence to an underwriting decision</h2><ol class="hew-process" aria-label="Analytical process">'+process.map(function(s,i){return '<li><span>'+String(i+1).padStart(2,'0')+'</span>'+s+'</li>';}).join('')+'</ol><p>The working hypothesis is that an asking-rent premium can narrow after lease incentives and operating costs. The analysis tests that mechanism without treating selected observations as a full rent roll.</p><dl class="decision-context"><div><dt>Decision</dt><dd>Which income and cost assumptions need verification before an investor underwrites a newly developed Brighton rental property?</dd></div><div><dt>Method</dt><dd>Compare lease-level economics, identify expense responsibility, reconcile the public tax record, and test one model driver at a time.</dd></div><div><dt>Boundary</dt><dd>Observed Hew evidence and hypothetical development outputs are separate. The analysis does not establish an acquisition price or actual Hew NOI.</dd></div></dl>',
 '<h2 class="case-section-title">Lease observations and public records answer different questions</h2>'+m.comparables+m.lease+m.tax+history()+context(),
 '<h2 class="case-section-title">Separate property evidence from scenario economics</h2>'+m.results+m.formulas+m.opex+m.inputs+m.sensitivity,
 '<h2 class="case-section-title">Underwrite the collected income and document the costs</h2>'+m.findings,
 '<h2 class="case-section-title">What is known, assumed and still missing</h2>'+m.limits
 ];
 return '<div class="page research-case study-report hew-report" data-case="hew"><header class="wrap portfolio-case-head"><div class="crumbs"><a href="#/research">Research</a> / Hew at 1515</div><div class="eyebrow">BRIGHTON / MULTIFAMILY UNDERWRITING</div><h1>Hew at 1515:<br>Leasing &amp; Public Tax Research</h1><p class="case-top-takeaway">Effective rent and expense responsibility determine how an asking-rent story translates into income. Boston’s tax record provides a documented cost reference; the development pro forma remains a separate illustration.</p><p class="intro">Public records · Dated leasing observations · Excel pro forma · Sensitivity analysis</p><p class="report-source">Research cutoff: 26 October 2026. Public evidence, practitioner observations and model assumptions are identified alongside the results.</p><p class="hero-route"><a href="#/study" data-case-jump="case-findings">Read the findings ↓</a> &nbsp; <a href="#/study" data-case-jump="case-evidence">Review the evidence ↓</a></p></header><div class="case-navigation"><div class="wrap"><nav class="case-contents" aria-label="Case study contents">'+sections.map(function(s,i){return '<a href="#/study" data-case-jump="case-'+s[0]+'"><span>'+String(i+1).padStart(2,'0')+'</span> '+['Question','Framework','Evidence','Analysis','Findings','Sources'][i]+'</a>';}).join('')+'</nav><label class="mobile-contents">Report section<select id="case-section-select">'+sections.map(function(s,i){return '<option value="case-'+s[0]+'">'+String(i+1).padStart(2,'0')+' / '+s[1]+'</option>';}).join('')+'</select></label></div></div>'+sections.map(function(s,i){return section(s[0],s[1],bodies[i],i);}).join('')+'</div>';
}
function mount(){
 destroy();
 if(!document.querySelector('.hew-report'))return;
 scrollHandler=function(){
  var nav=document.querySelector('.case-navigation'),limit=nav.getBoundingClientRect().height+56;
  var list=Array.from(document.querySelectorAll('.case-section')),active=list[0];
  list.forEach(function(el){if(el.getBoundingClientRect().top<=limit)active=el;});
  if(!active)return;
  document.querySelectorAll('.case-contents [data-case-jump]').forEach(function(a){var on=a.dataset.caseJump===active.id;a.classList.toggle('active',on);if(on)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');});
  document.getElementById('case-section-select').value=active.id;
 };
 window.addEventListener('scroll',scrollHandler,{passive:true});scrollHandler();
 var details=document.getElementById('hew-context'),mounted=false;
 if(details)details.addEventListener('toggle',function(){if(details.open&&!mounted){mounted=true;window.CyanStudy.mount();}else if(details.open){window.dispatchEvent(new Event('resize'));}});
 var body=document.getElementById('compBody');if(body){var table=body.closest('table');table.querySelector('thead tr').children[2].textContent='Actual occupancy';Array.from(body.rows).forEach(function(row){row.cells[2].textContent='Not established';});}
}
window.CyanHew={render:render,mount:mount,destroy:destroy,question:question};
})();
