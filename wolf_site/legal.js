function renderLegal(file){
 var esc=function(s){return String(s).replace(/[&<>]/g,function(m){return{"&":"&amp;","<":"&lt;",">":"&gt;"}[m]})};
 var inl=function(s){return esc(s).replace(/\*\*(.+?)\*\*/g,"<b>$1</b>")};
 fetch(file+"?v="+Date.now()).then(function(r){if(!r.ok)throw 0;return r.text()}).then(function(t){
  var out="",ul=false;
  t.split(/\r?\n/).forEach(function(l){
   if(/^\s*-\s+/.test(l)){if(!ul){out+="<ul>";ul=true}out+="<li>"+inl(l.replace(/^\s*-\s+/,""))+"</li>";return}
   if(ul){out+="</ul>";ul=false}
   if(/^# /.test(l))out+="<h1>"+inl(l.slice(2))+"</h1>";
   else if(/^## /.test(l))out+="<h2>"+inl(l.slice(3))+"</h2>";
   else if(/^\[DRAFT\]/.test(l))out+='<div class="draft">'+inl(l.replace("[DRAFT]","DRAFT:"))+"</div>";
   else if(l.trim())out+="<p>"+inl(l)+"</p>"});
  if(ul)out+="</ul>";document.getElementById("m").innerHTML=out+'<p><a href="./">Back to Wolf</a></p>'
 }).catch(function(){document.getElementById("m").innerHTML="<p>This page is not ready yet.</p>"})}
