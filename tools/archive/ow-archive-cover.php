<?php
/** Shop / category / brand archive hero: per-category cover image instead of the old demo image (wp-image-48).
 *  Override per term with term meta _ow_cover_id (attachment ID). Live as Code Snippet #12. */
add_filter('render_block', function($html,$block){
  if(is_admin() || strpos($html,'ow-sa-hero-bg')===false || ($block['blockName']??'')!=='core/image') return $html;
  $map=['dates'=>847,'khalas'=>905,'sukkari'=>956,'saqai'=>903,'medjool'=>906,'rushudiya'=>903,'date-paste'=>909,'stuffed-dates'=>908,'other-dates'=>847,
        'from-the-oasis'=>904,'luxury-serving-boxes'=>904,'maamoul'=>909,'coffee'=>907,'dibs'=>847,'tahini'=>847];
  $id=847; $alt='';
  $t=get_queried_object();
  if($t instanceof WP_Term){
    $alt=$t->name; $cur=$t;
    while($cur){
      $m=(int)get_term_meta($cur->term_id,'_ow_cover_id',true); if($m){$id=$m;break;}
      $slug=preg_replace('/-en$/','',$cur->slug); if(isset($map[$slug])){$id=$map[$slug];break;}
      $cur=$cur->parent?get_term($cur->parent,$cur->taxonomy):null;
    }
  }
  $img=wp_get_attachment_image($id,'full',false,['class'=>'wp-image-'.$id.' ow-sa-cover','fetchpriority'=>'high','loading'=>'eager','decoding'=>'async','alt'=>$alt?:get_bloginfo('name'),'sizes'=>'100vw']);
  if(!$img) return $html;
  return preg_replace('/<img[^>]*>/',$img,$html,1);
},20,2);
add_action('wp_head', function(){ ?>
<style id="ow-sa-cover-css">
.ow-sa-hero .ow-sa-cover{object-position:50% 45%}
.ow-sa-hero::after{background:linear-gradient(180deg,rgba(245,241,232,.62) 0%,rgba(245,241,232,.80) 50%,rgba(245,241,232,.92) 100%)!important}
.ow-sa-hero .ow-sa-hero-in,.ow-sa-hero .ow-sa-hero-in *{color:#1f3d2e!important;text-shadow:none!important}
.ow-sa-hero .ow-sa-lead-txt a{color:#a8761c!important;text-decoration:underline}
.ow-sa-hero .wd-delimiter{opacity:.5}
</style>
<?php });
