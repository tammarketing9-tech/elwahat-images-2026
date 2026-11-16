<?php
/** Home (mobile): categories as two marquee rows moving in opposite directions. Source: .ow-hm-catcar items.
 *  Live as Code Snippet #11 on elwahat.com. Empty categories (0 products) are skipped. */
add_action('wp_footer', function(){ if(!is_front_page()) return; ?>
<style id="ow-catmq-css">
@media (max-width:768px){
 .ow-hm-catcar.ow-catmq-on{display:none!important}
 .ow-catmq{display:flex;flex-direction:column;gap:14px;margin:6px -16px 0;overflow:hidden;direction:ltr;-webkit-mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent);mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent)}
 .ow-catmq-row{display:flex;width:max-content;gap:14px;animation:owmq var(--d,40s) linear infinite;will-change:transform}
 .ow-catmq-row.rev{animation-name:owmq-rev}
 .ow-catmq:hover .ow-catmq-row,.ow-catmq.paused .ow-catmq-row{animation-play-state:paused}
 .ow-catmq-i{flex:0 0 auto;width:104px;text-align:center;text-decoration:none;direction:rtl}
 .ow-catmq-i .im{display:block;width:96px;height:96px;margin:0 auto 7px;border-radius:50%;overflow:hidden;background:#fff;box-shadow:0 4px 14px rgba(31,93,58,.12);border:3px solid #fff;outline:1px solid rgba(200,150,46,.35)}
 .ow-catmq-i img{width:100%;height:100%;object-fit:cover;display:block}
 .ow-catmq-i .t{display:block;font-size:13px;font-weight:700;color:#1f2a24;line-height:1.3;white-space:nowrap}
 @keyframes owmq{from{transform:translateX(0)}to{transform:translateX(-50%)}}
 @keyframes owmq-rev{from{transform:translateX(-50%)}to{transform:translateX(0)}}
 @media (prefers-reduced-motion:reduce){.ow-catmq-row{animation:none}.ow-catmq{overflow-x:auto}}
}
</style>
<script id="ow-catmq-js">
(function(){
 function build(){
  if(window.innerWidth>768) return;
  var src=document.querySelector('.ow-hm-catcar'); if(!src||document.querySelector('.ow-catmq')) return;
  var seen={},items=[];
  src.querySelectorAll('.wd-cat').forEach(function(c){
   var a=c.querySelector('a[href]'),img=c.querySelector('img'),t=c.querySelector('h3'),n=c.querySelector('.wd-cat-count');
   if(!a||!t) return; var href=a.getAttribute('href'); if(seen[href]) return; seen[href]=1;
   var cnt=parseInt((n&&n.textContent||'').replace(/[^0-9]/g,''),10); if(n&&cnt===0) return;
   items.push({h:href,s:img?(img.currentSrc||img.getAttribute('src')):'',t:t.textContent.trim()});
  });
  if(items.length<4) return;
  var half=Math.ceil(items.length/2),rows=[items.slice(0,half),items.slice(half)];
  var wrap=document.createElement('div'); wrap.className='ow-catmq'; wrap.setAttribute('aria-label',src.getAttribute('aria-label')||'categories');
  rows.forEach(function(r,i){
   var row=document.createElement('div'); row.className='ow-catmq-row'+(i?' rev':''); row.style.setProperty('--d',(r.length*5)+'s');
   var html=r.map(function(x){return '<a class="ow-catmq-i" href="'+x.h+'"><span class="im"><img loading="lazy" src="'+x.s+'" alt=""></span><span class="t">'+x.t+'</span></a>';}).join('');
   row.innerHTML=html+html.replace(/<a /g,'<a aria-hidden="true" tabindex="-1" ');
   wrap.appendChild(row);
  });
  src.parentNode.insertBefore(wrap,src); src.classList.add('ow-catmq-on');
  wrap.addEventListener('touchstart',function(){wrap.classList.add('paused')},{passive:true});
  wrap.addEventListener('touchend',function(){setTimeout(function(){wrap.classList.remove('paused')},1200)},{passive:true});
 }
 if(document.readyState!=='loading') build(); else document.addEventListener('DOMContentLoaded',build);
})();
</script>
<?php }, 99);
