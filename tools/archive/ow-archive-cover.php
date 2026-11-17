<?php
/** Shop / category / brand archive hero: per-category cover banners (desktop + mobile) replacing the old demo image (wp-image-48).
 *  Override per term with term meta _ow_cover_id (desktop) and _ow_cover_m_id (mobile). Live as Code Snippet #12.
 *  Source images: covers/ in this repo (Gemini designs, 2026-11-17). */
add_filter('render_block', function($html,$block){
  if(is_admin() || strpos($html,'ow-sa-hero-bg')===false || ($block['blockName']??'')!=='core/image') return $html;
  $set=['all'=>[1073,1074],'sukkari'=>[1075,1076],'khalas'=>[1077,1078],'medjool'=>[1079,1080],'saqai'=>[1081,1082],'paste'=>[1083,1084],'gift'=>[1085,1086],'coffee'=>[1087,1088]];
  $map=['dates'=>'all','other-dates'=>'all','khalas'=>'khalas','sukkari'=>'sukkari','saqai'=>'saqai','rushudiya'=>'saqai','medjool'=>'medjool',
        'date-paste'=>'paste','dibs'=>'paste','tahini'=>'paste','maamoul'=>'paste','stuffed-dates'=>'gift','luxury-serving-boxes'=>'gift','from-the-oasis'=>'gift','coffee'=>'coffee'];
  $ids=$set['all']; $alt='';
  $t=get_queried_object();
  if($t instanceof WP_Term){
    $alt=$t->name; $cur=$t;
    while($cur){
      $d=(int)get_term_meta($cur->term_id,'_ow_cover_id',true); if($d){$m=(int)get_term_meta($cur->term_id,'_ow_cover_m_id',true);$ids=[$d,$m?:$d];break;}
      $slug=preg_replace('/-en$/','',$cur->slug); if(isset($map[$slug])){$ids=$set[$map[$slug]];break;}
      $cur=$cur->parent?get_term($cur->parent,$cur->taxonomy):null;
    }
  }
  $alt=$alt?:get_bloginfo('name');
  $d=wp_get_attachment_image($ids[0],'full',false,['class'=>'ow-sa-cover ow-cv-d','fetchpriority'=>'high','loading'=>'eager','decoding'=>'async','alt'=>$alt]);
  $m=wp_get_attachment_image($ids[1],'full',false,['class'=>'ow-sa-cover ow-cv-m','loading'=>'lazy','decoding'=>'async','alt'=>$alt]);
  if(!$d) return $html;
  return preg_replace('/<img[^>]*>/',$d.$m,$html,1);
},20,2);
add_action('wp_head', function(){ ?>
<style id="ow-sa-cover-css">
.ow-sa-hero .ow-sa-hero-bg{position:absolute;inset:0;margin:0}
.ow-sa-hero .ow-sa-cover{width:100%;height:100%;object-fit:cover;display:block}
.ow-sa-hero .ow-cv-d{object-position:0% 60%}
.ow-sa-hero .ow-cv-m{display:none;object-position:50% 100%}
.ow-sa-hero::after{background:linear-gradient(270deg,rgba(18,12,7,.92) 0%,rgba(18,12,7,.78) 38%,rgba(18,12,7,.25) 68%,rgba(18,12,7,0) 85%)!important}
html[dir="ltr"] .ow-sa-hero::after{background:linear-gradient(90deg,rgba(18,12,7,.92) 0%,rgba(18,12,7,.78) 38%,rgba(18,12,7,.25) 68%,rgba(18,12,7,0) 85%)!important}
.ow-sa-hero .ow-sa-hero-in{text-align:start;margin-inline-start:0;max-width:min(620px,52%)!important;padding-inline:clamp(20px,5vw,72px)}
.ow-sa-hero .ow-sa-hero-in,.ow-sa-hero .ow-sa-hero-in *{color:#F5F1E8!important;text-shadow:0 1px 12px rgba(0,0,0,.35)}
.ow-sa-hero .ow-sa-crumbs .wd-breadcrumbs{justify-content:flex-start}
.ow-sa-hero .ow-sa-lead-txt{color:#E8D9BC!important}
.ow-sa-hero .ow-sa-lead-txt a{color:#D99A5B!important;text-decoration:underline}
.ow-sa-hero .wd-delimiter{opacity:.6}
@media (max-width:768px){
 .ow-sa-hero{min-height:600px!important;display:flex;flex-direction:column;justify-content:flex-start}
 .ow-sa-hero .ow-cv-d{display:none}
 .ow-sa-hero .ow-cv-m{display:block}
 .ow-sa-hero::after{background:linear-gradient(180deg,rgba(18,12,7,.9) 0%,rgba(18,12,7,.72) 40%,rgba(18,12,7,.15) 70%,rgba(18,12,7,0) 85%)!important}
 .ow-sa-hero .ow-sa-hero-in{max-width:none!important;text-align:center;padding:26px 18px 0}
 .ow-sa-hero .ow-sa-crumbs .wd-breadcrumbs{justify-content:center}
}
</style>
<?php });
