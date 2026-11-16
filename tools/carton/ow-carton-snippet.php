<?php
/**
 * OW Carton pricing — حبة / كرتون
 * Meta: _ow_carton_qty (int), _ow_carton_price (float). Product price stays the unit price.
 * Cart: ?add-to-cart=ID&ow_pack=carton  → line price = carton price, label "كرتون N حبات".
 */
if (!function_exists('ow_ct_lang')) {
function ow_ct_lang(){ return function_exists('pll_current_language') ? pll_current_language() : 'ar'; }
function ow_ct_data($p){
  $p = is_numeric($p) ? wc_get_product($p) : $p; if(!$p) return null;
  $q=(int)$p->get_meta('_ow_carton_qty'); $c=(float)$p->get_meta('_ow_carton_price');
  if($q<2||$c<=0) return null;
  $u=(float)$p->get_price(); $save=($u>0)?round((1-($c/($u*$q)))*100):0;
  return ['qty'=>$q,'price'=>$c,'per'=>round($c/$q,2),'save'=>max(0,$save)];
}
function ow_ct_t($k,$q=0){
  $en=ow_ct_lang()==='en';
  $t=['unit'=>$en?'per piece':'للحبة','carton'=>$en?"Carton of $q":"كرتون $q حبات",'buy'=>$en?'Add carton to cart':'أضف الكرتون للسلة',
      'each'=>$en?'per piece in carton':'سعر الحبة في الكرتون','pack'=>$en?'Pack':'العبوة','piece'=>$en?'Piece':'حبة','wh'=>$en?'Wholesale by the carton':'جملة بالكرتون'];
  return $t[$k];
}
/* 1) Category / shop cards: carton pill under the price */
add_action('woocommerce_after_shop_loop_item_title', function(){
  global $product; $d=ow_ct_data($product); if(!$d) return;
  $url=esc_url(add_query_arg(['add-to-cart'=>$product->get_id(),'ow_pack'=>'carton'], wc_get_cart_url()));
  echo '<div class="ow-ct-pill"><span class="ow-ct-unit">'.esc_html(ow_ct_t('unit')).'</span>'
     .'<a class="ow-ct-btn" href="'.$url.'" rel="nofollow"><b>'.esc_html(ow_ct_t('carton',$d['qty'])).'</b> '.wc_price($d['price']).'</a></div>';
}, 11);
/* 2) Product page: prominent carton box after the normal add-to-cart form */
add_action('woocommerce_after_add_to_cart_form', function(){
  global $product; $d=ow_ct_data($product); if(!$d) return; ?>
  <form class="ow-ct-box" method="post" action="<?php echo esc_url($product->get_permalink()); ?>">
    <div class="ow-ct-head"><span class="ow-ct-tag"><?php echo esc_html(ow_ct_t('wh')); ?></span>
      <?php if($d['save']>0): ?><span class="ow-ct-save">-<?php echo (int)$d['save']; ?>%</span><?php endif; ?></div>
    <div class="ow-ct-main"><strong><?php echo esc_html(ow_ct_t('carton',$d['qty'])); ?></strong>
      <span class="ow-ct-price"><?php echo wc_price($d['price']); ?></span></div>
    <div class="ow-ct-sub"><?php echo esc_html(ow_ct_t('each')); ?>: <?php echo wc_price($d['per']); ?></div>
    <div class="ow-ct-row"><input type="number" name="quantity" value="1" min="1" step="1" inputmode="numeric" class="ow-ct-qty" aria-label="qty">
      <input type="hidden" name="add-to-cart" value="<?php echo (int)$product->get_id(); ?>"><input type="hidden" name="ow_pack" value="carton">
      <button type="submit" class="button ow-ct-submit"><?php echo esc_html(ow_ct_t('buy')); ?></button></div>
  </form><?php
}, 5);
/* 3) Cart logic */
add_filter('woocommerce_add_cart_item_data', function($data,$pid){
  if(!empty($_REQUEST['ow_pack']) && $_REQUEST['ow_pack']==='carton' && ow_ct_data($pid)) $data['ow_pack']='carton';
  return $data; },10,2);
add_action('woocommerce_before_calculate_totals', function($cart){
  if(is_admin() && !defined('DOING_AJAX')) return;
  foreach($cart->get_cart() as $it){ if(($it['ow_pack']??'')!=='carton') continue;
    $d=ow_ct_data($it['data']->get_id()); if($d) $it['data']->set_price($d['price']); }
},20);
add_filter('woocommerce_get_item_data', function($meta,$it){
  $d=ow_ct_data($it['product_id']);
  $meta[]=['key'=>ow_ct_t('pack'),'value'=>(($it['ow_pack']??'')==='carton'&&$d)?ow_ct_t('carton',$d['qty']):ow_ct_t('piece')];
  return $meta; },10,2);
add_action('woocommerce_checkout_create_order_line_item', function($item,$key,$values){
  if(($values['ow_pack']??'')==='carton'){ $d=ow_ct_data($values['product_id']); if($d) $item->add_meta_data('العبوة','كرتون '.$d['qty'].' حبات',true); }
},10,3);
/* 4) Styles */
add_action('wp_head', function(){ ?>
<style id="ow-ct-css">
.ow-ct-pill{display:flex;align-items:center;justify-content:space-between;gap:6px;margin:4px 0 6px;font-size:12px}
.ow-ct-unit{color:#6b6b6b}
.ow-ct-btn{display:inline-flex;gap:4px;align-items:center;padding:3px 9px;border:1px solid #c8962e;border-radius:999px;color:#1f5d3a;background:#fff8e8;font-size:12px;line-height:1.6;white-space:nowrap}
.ow-ct-btn:hover{background:#c8962e;color:#fff}.ow-ct-btn:hover .amount{color:#fff}
.ow-ct-btn .amount{font-weight:700;color:#1f5d3a}
.ow-ct-box{margin:14px 0 6px;padding:14px 16px;border:2px solid #c8962e;border-radius:14px;background:linear-gradient(180deg,#fffaf0,#fff)}
.ow-ct-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px}
.ow-ct-tag{font-size:12px;font-weight:700;color:#fff;background:#1f5d3a;padding:2px 10px;border-radius:999px}
.ow-ct-save{font-size:12px;font-weight:700;color:#a62620;background:#fde8e6;padding:2px 8px;border-radius:999px}
.ow-ct-main{display:flex;justify-content:space-between;align-items:baseline;gap:8px}
.ow-ct-main strong{font-size:17px;color:#1f5d3a}.ow-ct-price .amount{font-size:22px;font-weight:800;color:#1f5d3a}
.ow-ct-sub{font-size:12.5px;color:#666;margin:2px 0 10px}
.ow-ct-row{display:flex;gap:8px}.ow-ct-qty{width:70px!important;text-align:center}
.ow-ct-submit{flex:1;background:#c8962e!important;color:#fff!important;border-radius:10px!important;font-weight:700}
</style><?php });
}
