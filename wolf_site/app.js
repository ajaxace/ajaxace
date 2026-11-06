"use strict";
const CY="#2ec5ff",TL="#14e0c0",OR="#fca311",COL=[CY,TL,OR];
const $=id=>document.getElementById(id);
const esc=s=>String(s==null?"":s).replace(/[&<>"]/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[m]));
const el=(t,c,h)=>{const e=document.createElement(t);if(c)e.className=c;if(h!=null)e.innerHTML=h;return e};
const pad=n=>String(n).padStart(2,"0"),iso=d=>d.getFullYear()+"-"+pad(d.getMonth()+1)+"-"+pad(d.getDate()),hm=d=>pad(d.getHours())+":"+pad(d.getMinutes());
const DN=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],MN=["January","February","March","April","May","June","July","August","September","October","November","December"],DAYS=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"];
const TZ=(()=>{try{return Intl.DateTimeFormat().resolvedOptions().timeZone||""}catch(e){return""}})();
const lget=k=>{try{return localStorage.getItem(k)}catch(e){return null}},lset=(k,v)=>{try{localStorage.setItem(k,v)}catch(e){}};
let S={ver:0,people:{adults:[],kids:[]},hasKey:false,hasIcs:false,code:"",members:[],me:"",support:""};
let D={ev:[],shop:[],rem:[],notes:[],chores:[],meals:[],rota:[],photos:[],ics:[]};
let authed=false,busy=false,syncing=false,cur=null;
async function api(a,o={}){const x={method:o.body||o.form?"POST":"GET",credentials:"same-origin",headers:{"X-Wolf":"1"}};
 if(o.body){x.headers["Content-Type"]="application/json";x.body=JSON.stringify(o.body)}if(o.form)x.body=o.form;
 let r;try{r=await fetch("api.php?a="+a+(o.qs||""),x)}catch(e){const er=new Error("You seem to be offline.");er.status=0;throw er}
 let j={};try{j=await r.json()}catch(e){}
 if(!r.ok||j.ok===false){const er=new Error(j.error||"Something went wrong. Try again.");er.status=r.status;throw er}return j}
function toast(m){const t=$("toast");t.textContent=m;t.classList.add("on");clearTimeout(toast.h);toast.h=setTimeout(()=>t.classList.remove("on"),6000)}
function tick(){const n=new Date();$("clock").textContent=DN[n.getDay()].slice(0,3)+" "+n.getDate()+" "+MN[n.getMonth()].slice(0,3)+" · "+hm(n)}
tick();setInterval(tick,15000);
function ago(ts){const m=Math.round((Date.now()-ts)/60000);if(m<1)return"just now";if(m<60)return m+" min ago";const h=Math.round(m/60);if(h<24)return h+" h ago";return Math.round(h/24)+" d ago"}
const money=p=>"£"+((p||0)/100).toFixed(2);
function mondayOf(d){const m=new Date(d);m.setHours(0,0,0,0);m.setDate(m.getDate()-((m.getDay()+6)%7));return m}
function fmtDay(s){const d=new Date(s+"T00:00:00");return DN[d.getDay()].slice(0,3)+" "+d.getDate()+" "+MN[d.getMonth()].slice(0,3)}
/* ---------- data actions ---------- */
async function put(col,obj){const r=await api("put",{body:{col,obj}});await sync(true);return r.id}
async function upd(col,id,patch){await api("upd",{body:{col,id,patch}});await sync(true)}
async function del(col,id){await api("del",{body:{col,id}});await sync(true)}
async function sync(force){if(!authed||syncing)return;syncing=true;
 try{const j=await api("sync",{qs:"&since="+(force?0:S.ver)+"&tz="+encodeURIComponent(TZ)});showNotice(j.notice);if(j.same)return;
  S.ver=j.ver;S.people=j.people||{adults:[],kids:[]};S.hasKey=j.hasKey;S.hasIcs=j.hasIcs;S.code=j.code;S.members=j.members||[];S.me=j.me;
  ["ev","shop","rem","notes","chores","meals","rota"].forEach(c=>D[c]=j.data[c]||[]);D.photos=j.photos||[];D.ics=j.ics||[];renderAll()}
 catch(e){if(e.status===401){authed=false;showWelcome()}}finally{syncing=false}}
setInterval(()=>{if(!document.hidden)sync()},15000);document.addEventListener("visibilitychange",()=>{if(!document.hidden)sync()});
function showNotice(t){const n=$("notice");if(!n)return;n.textContent=t||"";n.hidden=!t}
/* ---------- welcome ---------- */
function showWelcome(){$("welcome").classList.add("on");$("boot").classList.remove("on")}
function nameOk(){const n=$("wname").value.trim();if(!n){$("werr").textContent="Please type your first name.";$("wname").focus();return null}return n}
$("wcreate").onclick=async()=>{const n=nameOk();if(!n)return;$("werr").textContent="";$("wcreate").disabled=true;try{await api("create",{body:{label:n}});await enter(true)}catch(e){$("werr").textContent=e.message}$("wcreate").disabled=false};
$("wjoin").onclick=async()=>{const n=nameOk();if(!n)return;const c=$("wcode").value.trim();if(c.length<6){$("werr").textContent="Enter your family code.";return}$("werr").textContent="";$("wjoin").disabled=true;try{await api("join",{body:{code:c,label:n}});await enter(false)}catch(e){$("werr").textContent=e.message}$("wjoin").disabled=false};
async function enter(first){authed=true;$("welcome").classList.remove("on");$("boot").classList.remove("on");await sync(true);if(first){go("setup","fam")}}
/* ---------- rendering ---------- */
function allEvents(){return D.ev.map(e=>Object.assign({ro:0},e)).concat(D.ics.map((e,i)=>({id:"i"+i,t:e.t,d:e.d,h:e.h,ro:1})))}
function renderWeek(){const w=$("week");w.innerHTML="";const A=S.people.adults||[];
 if(A.length){w.appendChild(el("h3",null,"School run · who has pick-up"));const rd=el("div","rota");["Mon","Tue","Wed","Thu","Fri"].forEach((n,k)=>{const r=D.rota.find(x=>x.day===k);rd.appendChild(el("button","rb "+(r?"dan":"none"),`<span>${n}</span><b>${r?esc(r.who):"?"}</b>`)).dataset.rd=k});w.appendChild(rd)}
 w.appendChild(el("h3",null,"This week · family calendar"));
 const mon=mondayOf(new Date()),todayIso=iso(new Date()),all=allEvents();
 for(let i=0;i<7;i++){const d=new Date(mon);d.setDate(mon.getDate()+i);const di=iso(d);const evs=all.filter(e=>e.d===di).sort((a,b)=>(a.h||"").localeCompare(b.h||""));
  w.appendChild(el("div","day",`<div class="dn ${di===todayIso?"today":""}"><span>${DN[d.getDay()].slice(0,3)}</span><b>${d.getDate()}</b></div><div class="evs">${evs.length?evs.map((e,k)=>`<div class="ev" style="--c:${COL[k%3]}"><span>${esc(e.t)}${e.ro?'<i class="ro">calendar</i>':""}</span><em>${esc(e.h||"")}</em>${e.ro?"":`<button data-del="${e.id}" aria-label="Remove">×</button>`}</div>`).join(""):'<div class="empty">Nothing planned</div>'}</div>`))}
 const endIso=iso(new Date(mon.getTime()+6*864e5)),later=all.filter(e=>e.d>endIso).sort((a,b)=>(a.d+a.h).localeCompare(b.d+b.h)).slice(0,25);
 if(later.length){w.appendChild(el("h3",null,"Later"));later.forEach(e=>w.appendChild(el("div","ev",`<span>${esc(e.t)}${e.ro?'<i class="ro">calendar</i>':""}</span><em>${fmtDay(e.d)} ${esc(e.h||"")}</em>${e.ro?"":`<button data-del="${e.id}" aria-label="Remove">×</button>`}`)))}
 const f=el("form","fadd","<input id=\"evt\" placeholder=\"Add an event, e.g. Dentist\"><button>Add</button><div class=\"r2\"><input id=\"evd\" type=\"date\"><input id=\"evh\" type=\"time\"></div>");f.id="evform";f.autocomplete="off";w.appendChild(f);
 f.onsubmit=e=>{e.preventDefault();const t=$("evt").value.trim(),d=$("evd").value;if(!t||!d){toast("Add a title and a date.");return}put("ev",{t:t.slice(0,80),d,h:$("evh").value||""}).catch(er=>toast(er.message))};
 w.onclick=ev=>{const r=ev.target.closest("[data-rd]");if(r){cycleRota(+r.dataset.rd);return}const b=ev.target.closest("[data-del]");if(b)del("ev",b.dataset.del).catch(er=>toast(er.message))}}
function cycleRota(day){const A=S.people.adults||[],r=D.rota.find(x=>x.day===day);let nx;if(!r)nx=A[0];else{const i=A.indexOf(r.who);nx=i>=0&&i<A.length-1?A[i+1]:""}
 (async()=>{if(!nx){if(r)await del("rota",r.id)}else if(r)await upd("rota",r.id,{who:nx});else await put("rota",{day,who:nx})})().catch(e=>toast(e.message))}
function listBlock(title,arr,key,form){return `<h3>${title}</h3>`+(arr.length?arr.map(i=>`<div class="li ${i.x?"done":""}"><input type="checkbox" data-k="${key}" data-id="${i.id}" ${i.x?"checked":""} aria-label="Done"><span>${esc(i.t)}${i.at?" · "+esc(remWhen(i)):""}</span><button data-k="${key}" data-rm="${i.id}" aria-label="Remove">×</button></div>`).join(""):'<div class="empty">Nothing here yet. Add one below, or ask Wolf.</div>')+form}
function remWhen(r){if(!r.at)return"";const d=new Date(r.at);return (iso(d)===iso(new Date())?"today":fmtDay(iso(d)))+" "+hm(d)}
function renderLists(){const l=$("lists");if(l.contains(document.activeElement)&&document.activeElement.tagName==="INPUT"&&document.activeElement.type==="text")return;
 const sf='<form class="fadd" id="shopform" autocomplete="off"><input id="shopinp" placeholder="Add to shopping list"><button>Add</button></form>';
 const rf='<form class="fadd" id="remform" autocomplete="off"><input id="reminp" placeholder="Remind us to…"><button>Add</button><div class="r2"><input id="remwhen" type="datetime-local"></div></form>';
 l.innerHTML=listBlock("Shopping",D.shop,"shop",sf)+listBlock("Reminders",D.rem.slice().sort((a,b)=>(a.at||9e15)-(b.at||9e15)),"rem",rf);
 $("shopform").onsubmit=e=>{e.preventDefault();const v=$("shopinp").value.trim();if(v)put("shop",{t:v.slice(0,60),x:0}).catch(er=>toast(er.message))};
 $("remform").onsubmit=e=>{e.preventDefault();const v=$("reminp").value.trim(),w=$("remwhen").value;if(v)put("rem",{t:v.slice(0,80),at:w?new Date(w).getTime():0,x:0}).catch(er=>toast(er.message))};
 l.onclick=ev=>{const c=ev.target.closest("input[data-id]"),r=ev.target.closest("[data-rm]");if(c)upd(c.dataset.k,c.dataset.id,{x:c.checked?1:0}).catch(er=>toast(er.message));if(r)del(r.dataset.k,r.dataset.rm).catch(er=>toast(er.message))}}
function renderNotes(){const l=$("nlist"),arr=D.notes.slice().sort((a,b)=>(b.ts||0)-(a.ts||0));
 l.innerHTML=arr.length?arr.map(n=>`<div class="note2"><p>${esc(n.t)}</p><small>${esc(n.by||"Family")} · ${ago(n.ts||n._ts*1000)}</small><button data-n="${n.id}" aria-label="Delete note">×</button></div>`).join(""):'<div class="empty">No notes yet. Write one above.</div>';
 l.onclick=ev=>{const b=ev.target.closest("[data-n]");if(b)del("notes",b.dataset.n).catch(er=>toast(er.message))}}
$("nform").onsubmit=e=>{e.preventDefault();const v=$("ninp").value.trim();if(!v)return;$("ninp").value="";put("notes",{t:v.slice(0,500),ts:Date.now()}).catch(er=>toast(er.message))};
function renderChores(){const K=S.people.kids||[];$("cwho").innerHTML=K.length?K.map(k=>`<option>${esc(k)}</option>`).join(""):"<option>Add children's names in Set-up</option>";
 $("kids").innerHTML=K.map(n=>{const e=D.chores.filter(c=>c.who===n&&c.x&&!c.paid).reduce((s,c)=>s+(c.v||0),0);return `<div class="kid"><b>${esc(n)}</b><em>${money(e)}</em><button data-pay="${esc(n)}">Mark paid</button></div>`}).join("")||'<div class="empty">Add your children\'s names in the set-up guide to use chores.</div>';
 $("clist").innerHTML=D.chores.length?D.chores.slice().sort((a,b)=>(a.x||0)-(b.x||0)).map(c=>`<div class="li ${c.x?"done":""}"><input type="checkbox" data-c="${c.id}" ${c.x?"checked":""} aria-label="Done"><span>${esc(c.t)} · ${esc(c.who)} · ${money(c.v)}${c.paid?" · paid":""}</span><button data-cr="${c.id}" aria-label="Remove">×</button></div>`).join(""):'<div class="empty">No chores yet. Add one above.</div>'}
$("kids").onclick=async e=>{const b=e.target.closest("[data-pay]");if(!b)return;try{for(const c of D.chores.filter(c=>c.who===b.dataset.pay&&c.x&&!c.paid))await api("upd",{body:{col:"chores",id:c.id,patch:{paid:1}}});await sync(true);toast(b.dataset.pay+" marked as paid.")}catch(er){toast(er.message)}};
$("clist").onclick=e=>{const c=e.target.closest("[data-c]"),r=e.target.closest("[data-cr]");if(c)upd("chores",c.dataset.c,{x:c.checked?1:0}).catch(er=>toast(er.message));if(r)del("chores",r.dataset.cr).catch(er=>toast(er.message))};
$("cform").onsubmit=e=>{e.preventDefault();const t=$("ctitle").value.trim();if(!t)return;if(!(S.people.kids||[]).length){toast("Add your children's names first.");return}const v=Math.round(parseFloat($("cval").value||"0")*100);$("ctitle").value="";put("chores",{t:t.slice(0,80),who:$("cwho").value,v:isNaN(v)?0:v,x:0,paid:0}).catch(er=>toast(er.message))};
function renderMeals(){const w=$("meals");if(w.contains(document.activeElement))return;
 w.innerHTML=DAYS.map((n,i)=>{const m=D.meals.find(x=>x.day===i)||{t:"",ing:""};return `<div class="meal"><div class="mh"><b>${n}</b><input data-md="${i}" data-f="t" value="${esc(m.t)}" placeholder="What's for dinner?"><button data-ms="${i}">+ Shopping</button></div><input data-md="${i}" data-f="ing" value="${esc(m.ing)}" placeholder="Ingredients, separated by commas"></div>`}).join("")}
$("meals").onchange=e=>{const i=e.target.closest("[data-md]");if(!i)return;const d=+i.dataset.md,m=D.meals.find(x=>x.day===d)||{t:"",ing:""},p={t:m.t||"",ing:m.ing||""};p[i.dataset.f]=i.value.trim();(async()=>{if(m.id)await upd("meals",m.id,{t:p.t,ing:p.ing});else if(p.t||p.ing)await put("meals",{day:d,t:p.t,ing:p.ing})})().catch(er=>toast(er.message))};
$("meals").onclick=async e=>{const b=e.target.closest("[data-ms]");if(!b)return;const m=D.meals.find(x=>x.day===+b.dataset.ms);const items=((m&&m.ing)||"").split(",").map(s=>s.trim()).filter(Boolean);if(!items.length){toast("Add some ingredients first.");return}let n=0;try{for(const it of items){if(D.shop.some(s=>!s.x&&String(s.t).toLowerCase()===it.toLowerCase()))continue;await api("put",{body:{col:"shop",obj:{t:it.slice(0,60),x:0}}});n++}await sync(true);toast(n?n+" item"+(n>1?"s":"")+" added to the shopping list.":"Those are already on the list.")}catch(er){toast(er.message)}};
async function shrink(file){try{const bm=await createImageBitmap(file);const s=Math.min(1,1600/Math.max(bm.width,bm.height));const c=document.createElement("canvas");c.width=Math.round(bm.width*s);c.height=Math.round(bm.height*s);c.getContext("2d").drawImage(bm,0,0,c.width,c.height);return await new Promise(r=>c.toBlob(r,"image/jpeg",.82))}catch(e){return file}}
async function addFiles(files){let n=0;for(const f of files){try{const blob=await shrink(f),fd=new FormData();fd.append("f",blob,"photo.jpg");await api("photo",{form:fd});n++}catch(e){toast(e.message)}}await sync(true);if(n)toast(n+" photo"+(n>1?"s":"")+" added to family storage.")}
["cam","gal"].forEach(id=>$(id).onchange=e=>{const fs=[...e.target.files];e.target.value="";if(fs.length)addFiles(fs)});
function renderPhotos(){const g=$("grid");g.innerHTML="";const p=D.photos.slice().sort((a,b)=>(b.ts||0)-(a.ts||0));
 $("smsg").textContent=p.length?p.length+" shared photo"+(p.length>1?"s":"")+" in your family storage.":"No photos yet. Tap Take photo and it appears for the whole family.";
 p.forEach(x=>{const b=el("button","ph",`<img loading="lazy" src="api.php?a=img&id=${encodeURIComponent(x.id)}" alt=""><i>${esc(x.by||"Family")} · ${ago(x.ts)}</i>`);b.onclick=()=>{cur=x;$("vimg").src="api.php?a=img&id="+encodeURIComponent(x.id);$("vdel").hidden=false;$("view").classList.add("on")};g.appendChild(b)})}
$("vclose").onclick=()=>$("view").classList.remove("on");
$("vdel").onclick=async()=>{if(!cur)return;const p=cur;$("view").classList.remove("on");try{await del("photos",p.id)}catch(e){toast(e.message)}};
function renderMore(){const pc=D.chores.filter(c=>!c.x).length;$("mc1").textContent=D.chores.length?(pc?pc+" to do":"All done"):"Pocket money for jobs done";const n=D.meals.filter(m=>m.t).length;$("mc2").textContent=n?n+" dinner"+(n>1?"s":"")+" planned":"Dinner plan to shopping list";$("mc3").textContent=D.notes.length?D.notes.length+" note"+(D.notes.length>1?"s":""):"Shared with the family";$("mc4").textContent=D.photos.length?D.photos.length+" photo"+(D.photos.length>1?"s":""):"Family storage"}
function renderFam(){$("fcode").textContent=S.code||"—";const n=S.members.length;$("fcount").textContent=n+" phone"+(n===1?"":"s")+" linked";$("s4code").textContent=S.code||"—";
 const P=(S.people.adults||[]).map(x=>[x,0]).concat((S.people.kids||[]).map(x=>[x,1]));
 $("people").innerHTML=P.length?P.map(([n,k])=>`<div class="mem"><div class="av ${k?"k":""}">${esc(n.slice(0,1).toUpperCase())}</div><div><b>${esc(n)}</b><span>${k?"Child":"Adult"}</span></div></div>`).join(""):'<div class="empty">Add your family\'s names in the set-up guide.</div>';
 $("pilltxt").textContent=n>1?n+" phones linked":"Family ready";
 const sup=S.support;$("support").href=sup?"mailto:"+sup:"#";$("s6mail").href=sup?"mailto:"+sup+"?subject=Wolf%20set-up%20help":"#";$("s6mail").hidden=!sup;$("s6vid").hidden=!S.video;if(S.video)$("s6vid").href=S.video;
 $("s1").classList.toggle("ok",S.hasKey);$("s2").classList.toggle("ok",!!((S.people.adults||[]).length||(S.people.kids||[]).length));$("s3").classList.toggle("ok",S.hasIcs||lget("wolf_skipcal")==="1");$("s4").classList.toggle("ok",n>1);$("s5").classList.toggle("ok",window.matchMedia&&matchMedia("(display-mode: standalone)").matches);
 if(document.activeElement!==$("p_ad")&&document.activeElement!==$("p_kid")){$("p_ad").value=(S.people.adults||[]).join(", ");$("p_kid").value=(S.people.kids||[]).join(", ")}
 renderCheck()}
function renderCheck(){const c=$("check");if(S.hasKey&&((S.people.adults||[]).length||(S.people.kids||[]).length)){c.innerHTML="";return}
 c.innerHTML=`<div class="check"><b>Finish setting up Wolf</b><br>${S.hasKey?"✓":"•"} Add your free AI key<br>${((S.people.adults||[]).length||(S.people.kids||[]).length)?"✓":"•"} Add your family's names<br><button class="btn sm" data-go="setup">Open the set-up guide</button></div>`}
function renderAll(){renderWeek();renderLists();renderNotes();renderChores();renderMeals();renderPhotos();renderMore();renderFam()}
/* ---------- navigation ---------- */
function go(id,navKey){document.querySelectorAll(".tab").forEach(t=>t.classList.toggle("on",t.id==="t-"+id));document.querySelectorAll("nav button").forEach(x=>x.classList.toggle("on",x.dataset.t===(navKey||id)));const m=document.querySelector("main");if(m)m.scrollTop=0}
document.addEventListener("click",e=>{const g=e.target.closest("[data-go]");if(g){const id=g.dataset.go;go(id,id==="setup"?"fam":(["chores","meals","notes","store"].includes(id)?"more":id))}});
document.querySelectorAll("nav button").forEach(b=>b.onclick=()=>go(b.dataset.t));
/* ---------- chat ---------- */
const chat=$("chat"),sugg=$("sugg"),q=$("q");
function say(text,who){chat.appendChild(el("div","b "+who,esc(text)));chat.scrollTop=chat.scrollHeight}
function answer(a){let h=esc(a.r);(a.c||[]).forEach(([l,v,c])=>h+=`<div class="chip" style="--c:${c}"><span>${esc(l)}</span><b>${esc(v)}</b></div>`);if(a.n)h+=`<small>${esc(a.n)}</small>`;const b=el("div","b wolf",h);chat.appendChild(b);chat.scrollTop=chat.scrollHeight;return b}
function dayList(di){return allEvents().filter(e=>e.d===di).sort((a,b)=>(a.h||"").localeCompare(b.h||""))}
function localAnswer(l){const n=new Date();
 if(/^(what'?s?( is)? the time|what time is it( now)?|time now|current time)\??$/.test(l))return{r:"It's "+hm(n)+" on "+DN[n.getDay()]+" "+n.getDate()+" "+MN[n.getMonth()]+".",n:"From your phone's clock."};
 if(/^(what'?s?( is)? (the )?(date|day)( today)?|what day is it|today'?s date)\??$/.test(l))return{r:"Today is "+DN[n.getDay()]+" "+n.getDate()+" "+MN[n.getMonth()]+" "+n.getFullYear()+".",n:"From your phone's clock."};
 if(/^who('?s| has| is| have)?.*(pick[- ]?up|school run|picking)/.test(l)&&!/\b(add|set|change|swap)\b/.test(l)){const wd=(n.getDay()+6)%7;if(wd>4)return{r:"No school run today.",n:"It's the weekend."};const r=D.rota.find(x=>x.day===wd);return r?{r:r.who+" has the school run today.",n:"From your family rota."}:{r:"Nobody is down for the school run today.",n:"Set it on the Week tab."}}
 if(/^(what'?s on )?(the |my |our )?shopping( list)?\??$|^what do we need\??$/.test(l)){const u=D.shop.filter(i=>!i.x);return{r:u.length?"On the list: "+u.map(i=>i.t.toLowerCase()).join(", ")+".":"The shopping list is empty.",n:"Add more on the Lists tab, or just ask."}}
 const m=l.match(/^(what'?s on|what have we got|what'?s happening|what'?s planned)( (today|tomorrow|this week))?\??$/);
 if(m){const w=m[3]||"today";if(w==="this week"){const t=iso(n),u=allEvents().filter(e=>e.d>=t&&e.d<=iso(new Date(n.getTime()+6*864e5))).sort((a,b)=>(a.d+a.h).localeCompare(b.d+b.h)).slice(0,6);return{r:u.length?"Coming up:":"Nothing planned this week.",c:u.map((e,k)=>[fmtDay(e.d).split(" ")[0],e.t+(e.h?" "+e.h:""),COL[k%3]]),n:"From your family calendar."}}
  const d=new Date(n);if(w==="tomorrow")d.setDate(d.getDate()+1);const u=dayList(iso(d));return{r:u.length?(w==="today"?"Today:":"Tomorrow:"):"Nothing planned "+w+".",c:u.map((e,k)=>[e.h||"All day",e.t,COL[k%3]]),n:"From your family calendar."}}
 return null}
function reply(fn){busy=true;const t=el("div","typing","<i></i><i></i><i></i>");chat.appendChild(t);chat.scrollTop=chat.scrollHeight;return new Promise(r=>setTimeout(()=>{t.remove();try{fn()}catch(e){}busy=false;r()},500))}
async function ask(text){text=(text||"").trim();if(!text||busy)return;say(text,"me");const l=text.toLowerCase().replace(/\s+/g," ");
 const la=localAnswer(l);if(la)return reply(()=>answer(la));
 if(!S.hasKey){return reply(()=>{const b=answer({r:"I need your free AI key before I can chat about that. It takes about 2 minutes.",n:""});const bt=el("button","btn sm","Open the set-up guide");bt.style.marginTop="8px";bt.dataset.go="setup";b.appendChild(bt)})}
 busy=true;const t=el("div","typing","<i></i><i></i><i></i>");chat.appendChild(t);chat.scrollTop=chat.scrollHeight;
 try{const j=await api("ai",{body:{message:text,tz:TZ}});t.remove();chat.appendChild(el("div","b wolf",esc(j.reply)));chat.scrollTop=chat.scrollHeight;sync(true)}
 catch(e){t.remove();answer({r:e.message,n:""})}busy=false}
[["What's on today?","What's on today?"],["Who has pick-up?","Who has pick-up today?"],["Shopping list","What's on the shopping list?"],["What's on this week?","What's on this week?"]].forEach(([s,v])=>{const b=el("button",null,esc(s));b.onclick=()=>ask(v);sugg.appendChild(b)});
{const b=el("button",null,"Remind me to…");b.onclick=()=>{q.value="Remind me to ";q.focus()};sugg.appendChild(b)}
$("f").onsubmit=e=>{e.preventDefault();const v=q.value;q.value="";ask(v)};
/* ---------- microphone ---------- */
const SR=window.SpeechRecognition||window.webkitSpeechRecognition;let rec=null;
$("mic").onclick=()=>{if(rec){try{rec.stop()}catch(e){}return}
 if(!SR){toast("Voice isn't available in this browser. Tap the mic on your keyboard instead.");q.focus();return}
 try{rec=new SR();rec.lang=navigator.language||"en-GB";rec.interimResults=true;rec.continuous=false;
  rec.onresult=e=>{let s="";for(const r of e.results)s+=r[0].transcript;q.value=s};
  rec.onerror=e=>{if(["not-allowed","service-not-allowed"].includes(e.error))toast("Allow the microphone for this site in your browser settings, or tap the mic on your keyboard.");else if(e.error==="no-speech")toast("I didn't hear anything. Try again.");else toast("Voice didn't work. Tap the mic on your keyboard instead.")};
  rec.onend=()=>{$("mic").classList.remove("rec");rec=null;const v=q.value.trim();if(v){q.value="";ask(v)}};
  rec.start();$("mic").classList.add("rec")}catch(e){rec=null;toast("Voice isn't available here. Tap the mic on your keyboard instead.");q.focus()}};
/* ---------- reminders (fire on each phone while Wolf is open) ---------- */
const fired=new Set((()=>{try{return JSON.parse(lget("wolf_fired")||"[]")}catch(e){return[]}})());
function beep(){try{const a=new (window.AudioContext||window.webkitAudioContext)(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=880;g.gain.value=.2;o.start();o.stop(a.currentTime+.4)}catch(e){}try{navigator.vibrate&&navigator.vibrate([300,150,300])}catch(e){}}
setInterval(()=>{const now=Date.now();D.rem.forEach(r=>{if(r.at&&!r.x&&!fired.has(r.id)&&r.at<=now&&now-r.at<864e5){fired.add(r.id);lset("wolf_fired",JSON.stringify([...fired].slice(-200)));beep();toast("Reminder: "+r.t)}})},10000);
/* ---------- set-up guide ---------- */
async function testKey(k){$("k_msg").style.color="";$("k_msg").textContent="Testing your key…";try{const j=await api("settings",{body:{ai_key:k}});$("k_msg").style.color="var(--tl)";$("k_msg").textContent="✓ "+(j.message||"Key saved.");$("k_inp").value="";await sync(true)}catch(e){$("k_msg").style.color="";$("k_msg").textContent=e.message}}
$("k_go").onclick=()=>{const k=$("k_inp").value.trim();if(k)testKey(k);else $("k_msg").textContent="Paste your key into the box first."};
$("k_paste").onclick=async()=>{try{const t=(await navigator.clipboard.readText()||"").trim();if(!t){$("k_msg").textContent="Nothing was copied yet. Copy the key first.";return}$("k_inp").value=t;testKey(t)}catch(e){$("k_msg").textContent="Your phone blocked pasting. Press and hold in the box below, tap Paste, then tap Test.";$("k_inp").focus()}};
$("p_save").onclick=async()=>{const sp=s=>s.split(",").map(x=>x.trim()).filter(Boolean);try{await api("people",{body:{adults:sp($("p_ad").value),kids:sp($("p_kid").value)}});await sync(true);toast("Names saved.")}catch(e){toast(e.message)}};
const CAL={g:["On a computer (or your phone in <b>Desktop site</b> mode), open calendar.google.com.","Tap the cog, then <b>Settings</b>.","Under <b>Settings for my calendars</b>, pick your calendar.","Open <b>Integrate calendar</b>.","Copy <b>Secret address in iCal format</b> and paste it below."],
 o:["Open Outlook on the web, then <b>Settings</b>, then <b>Calendar</b>.","Choose <b>Shared calendars</b>.","Under <b>Publish a calendar</b>, pick your calendar and <b>Can view all details</b>, then <b>Publish</b>.","Copy the <b>ICS</b> link and paste it below."],
 a:["Open iCloud.com and go to Calendar.","Tap the share icon next to your calendar.","Turn on <b>Public Calendar</b> and copy the link.","Paste it below."]};
let calTab="g";function renderCal(){$("calsteps").innerHTML=CAL[calTab].map((x,i)=>"<li>"+x+'<img class="gimg" src="guide/cal-'+calTab+"-"+(i+1)+'.jpg" alt="" loading="lazy" onerror="this.remove()"></li>').join("");document.querySelectorAll("[data-cal]").forEach(b=>b.classList.toggle("on",b.dataset.cal===calTab))}
document.querySelectorAll("[data-cal]").forEach(b=>b.onclick=()=>{calTab=b.dataset.cal;renderCal()});renderCal();
$("c_go").onclick=async()=>{let u=$("c_inp").value.trim().replace(/^webcal:/i,"https:");if(!u){$("c_msg").textContent="Paste your calendar link first.";return}$("c_msg").style.color="";$("c_msg").textContent="Connecting…";try{const j=await api("settings",{body:{ics_url:u,tz:TZ}});$("c_msg").style.color="var(--tl)";$("c_msg").textContent="✓ "+(j.message||"Connected.");$("c_inp").value="";await sync(true)}catch(e){$("c_msg").style.color="";$("c_msg").textContent=e.message}};
$("c_skip").onclick=()=>{lset("wolf_skipcal","1");renderFam();toast("Skipped. You can connect it later.")};
async function share(){const t="Join my family on Wolf. Open "+location.origin+location.pathname+" and enter the code "+S.code;try{if(navigator.share){await navigator.share({title:"Wolf",text:t})}else{await navigator.clipboard.writeText(t);toast("Invite copied.")}}catch(e){}}
$("sharebtn").onclick=share;$("s4share").onclick=share;
const copyCode=async()=>{try{await navigator.clipboard.writeText(S.code);toast("Code copied.")}catch(e){toast("Code: "+S.code)}};$("copybtn").onclick=copyCode;$("s4copy").onclick=copyCode;
let bip=null;window.addEventListener("beforeinstallprompt",e=>{e.preventDefault();bip=e;$("s5go").hidden=false});$("s5go").onclick=async()=>{if(bip){bip.prompt();bip=null}};
const arm=(b,msg,fn)=>{let t=0;b.onclick=()=>{if(t){fn();return}t=1;const o=b.textContent;b.textContent="Tap again to confirm";setTimeout(()=>{t=0;b.textContent=o},4000)}};
arm($("leavebtn"),"",async()=>{try{await api("leave",{body:{}})}catch(e){}authed=false;showWelcome()});
arm($("wipebtn"),"",async()=>{try{await api("wipe",{body:{}});authed=false;D={ev:[],shop:[],rem:[],notes:[],chores:[],meals:[],rota:[],photos:[],ics:[]};S.ver=0;showWelcome();toast("Your family's data was deleted.")}catch(e){toast(e.message)}});
arm($("codebtn"),"",async()=>{try{const j=await api("newcode",{body:{}});S.code=j.code;renderFam();toast("New code made. The old one no longer works.")}catch(e){toast(e.message)}});
$("fbsend").onclick=async()=>{const t=$("fbtxt").value.trim();if(!t){toast("Write something first.");return}try{await api("feedback",{body:{text:t}});$("fbtxt").value="";toast("Thank you. We read every message.")}catch(e){toast(e.message)}};
/* ---------- start ---------- */
if("serviceWorker"in navigator)addEventListener("load",()=>navigator.serviceWorker.register("sw.js").catch(()=>{}));
(async()=>{try{const j=await api("me");S.support=j.support||"";S.video=j.video||"";showNotice(j.notice);if(j.authed){authed=true;$("boot").classList.remove("on");await sync(true)}else showWelcome()}catch(e){showWelcome();$("werr").textContent="Can't reach Wolf right now. Check your connection."}})();
