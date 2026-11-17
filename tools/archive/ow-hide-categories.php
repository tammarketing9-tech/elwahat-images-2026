<?php
/** TEMP (Code Snippet #13): hide product categories coffee + maamoul across the front end.
 *  Deactivate the snippet to bring them back. Terms, products and settings stay untouched. */
function ow_hidden_cat_slugs(){ return ['coffee','coffee-en','maamoul','maamoul-en']; }
function ow_hidden_cat_ids(){ static $ids=null; if($ids!==null) return $ids; $ids=[];
  foreach(ow_hidden_cat_slugs() as $s){ $t=get_term_by('slug',$s,'product_cat'); if($t) $ids[]=(int)$t->term_id; } return $ids; }
function ow_hidden_href($html){ return (bool)preg_match('#/product-category/[^"\'>]*/(coffee|maamoul)(-en)?/?["\']#',$html); }
add_filter('get_terms', function($terms,$tax,$qv){
  if(is_admin() || !in_array('product_cat',(array)$tax,true) || !is_array($terms)) return $terms;
  $h=ow_hidden_cat_ids(); if(!$h) return $terms;
  return array_values(array_filter($terms,function($t)use($h){ return !(is_object($t) && in_array((int)$t->term_id,$h,true)); }));
},20,3);
add_filter('render_block', function($html,$block){
  if(is_admin()) return $html; $n=$block['blockName']??'';
  if(in_array($n,['core/list-item','core/image','core/navigation-link'],true) && ow_hidden_href($html)) return '';
  return $html; },20,2);
add_filter('wp_nav_menu_objects', function($items){
  $h=ow_hidden_cat_ids();
  return array_filter($items,function($i)use($h){ return !(($i->object==='product_cat' && in_array((int)$i->object_id,$h,true)) || ow_hidden_href('href="'.$i->url.'"')); }); });
add_action('template_redirect', function(){
  if(is_tax('product_cat')){ $t=get_queried_object(); if($t && in_array((int)$t->term_id,ow_hidden_cat_ids(),true)){ wp_safe_redirect(wc_get_page_permalink('shop'),302); exit; } } });
add_filter('rank_math/sitemap/entry', function($url,$type,$obj){
  if($type==='term' && is_object($obj) && isset($obj->term_id) && in_array((int)$obj->term_id,ow_hidden_cat_ids(),true)) return false; return $url; },10,3);
add_action('wp_head', function(){ echo '<style id="ow-hide-cats">li:has(> a[href*="/coffee/"][href*="product-category"]),li:has(> a[href*="/maamoul/"][href*="product-category"]),li:has(> a[href*="/coffee-en/"]),li:has(> a[href*="/maamoul-en/"]),a.pf-value[href*="/coffee"],a.pf-value[href*="/maamoul"]{display:none!important}</style>'; });
