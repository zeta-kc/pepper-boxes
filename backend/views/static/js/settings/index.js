jQuery(function ($) {
  //すべてのパネルを非表示
  $('#panel > dd').hide();
  //タイトル(dt)要素のイベントリスナー
  $(document).on("click",'#panel > dt' , (function () {
      //クリックされたdt要素の次のdd要素を取得
      var dd = $('+dd', this);
      //パネル(dd要素)が開いているか
      if (dd.css('display') === 'block') {
        dd.slideUp(500);//空いていれば閉じる
      } else {
        dd.slideDown(500);//閉じていれば開く
      }
    }));
});