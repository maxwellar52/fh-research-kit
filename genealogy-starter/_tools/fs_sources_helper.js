// FamilySearch source reader, shared by fh-family-evaluation and rerun-ancestor-log.
// Run this whole file once per session in javascript_tool on any familysearch.org page.
// It saves the helper in the site's localStorage as __x. Then, on a person's Details page, run:
//   await (new (Object.getPrototypeOf(async function(){}).constructor)(localStorage.__x))()
// and read the result with get_page_text: the vitals plus one compact line per attached source (first 22).
localStorage.__x = String.raw`await new Promise(r=>setTimeout(r,2500));
const main=document.querySelector('main').innerText;
const vit=main.split('Sources (')[0].replace(/Quality Score[\s\S]*?Vitals\n/,'').replace(/Last Changed:[^\n]*\n[A-Z]\n[^\n]*\n/g,'').replace(/Detail View\n/g,'').replace(/\n•\n/g,' ').replace(/\n+/g,' | ');
const btns=[...document.querySelectorAll('button')].filter(b=>/^\d{4}\s*•/.test(b.innerText.trim()));
const drop=/^(Book Number|Line Number|Page Number|Piece\/Folio|Registration Number|Household Identifier|Event Type|Event Place \(Original\)|Folio Number.*|Sub-District.*|Enumeration District|District Number|Record Type|Document Type|Source Page Type|Schedule Type|Series Name|Source Details|Affiliate Film Number|Entry Number)$/;
const out=[];
for(const b of btns.slice(0,22)){ b.click(); await new Promise(r=>setTimeout(r,1300));
 const h=[...document.querySelectorAll('h2,h3,div')].find(e=>e.innerText?.trim()==='Source Information');
 let p=h; for(let i=0;i<6&&p;i++){p=p.parentElement; if(p.innerText.length>300) break;}
 let t=(p?p.innerText:'').replace(/Citation Details[\s\S]*/,'').replace(/Source Date\n[\s\S]*?(Reason This Source Is Attached:)/,'$1').replace(/https?:\S+/g,'').replace(/[?&=]/g,' ');
 const L=t.split('\n').map(x=>x.trim()).filter(x=>x&&!/^(Source Information|VIEW|EDIT|REVIEW ATTACHMENTS|DETACH|Tags|\+ ADD TAG|\+ ADD|DISMISS|VIEW IMAGE|VIEW ORIGINAL DOCUMENT|Check Image Availability|Image Unavailable|No Image Available|No reason provided\.|Reason This Source Is Attached:|Birth|Sex|Name|Death|Burial|Marriage|Christening|Relationships|Residence|Male|Female|UNFINISHED ATTACHMENTS|This source has not been attached to all people found in the record\.)$/.test(x)&&!/person details$|^View on/.test(x));
 const o=[];for(let i=0;i<L.length;i++){if(drop.test(L[i])){i++;continue;}o.push(L[i]);}
 out.push(o.join('|').replace(/Birth Year \(Estimated\)/g,'BYE').replace(/Relationship to Head of Household/g,'Rel').replace(/Event Place/g,'Pl').replace(/Event Date/g,'Dt'));
}
const m=document.querySelector('main'); const pre=document.createElement('pre');
pre.textContent='VITALS: '+vit+'\nSOURCES('+btns.length+'):\n'+out.map((s,i)=>i+') '+s).join('\n');
m.innerHTML=''; m.appendChild(pre); return 'ok '+btns.length;`; 'saved'
