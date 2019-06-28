// $(document).ready(function() {
//   $('#form').on('submit',function(event){
//     $.ajax({
//       data : {
//         firstname : $('#firstname').val(),
//         lastname: $('#lastname').val(),
//       },
//       type : 'POST',
//       url : '/'
//     })
//     .done(function(data){
//       $('#output').text(data.output).show();
//     });
//     event.preventDefault();
//   });
// });
// $(document).ready(function(){
//   $('#post_file_btn').on('click',function(){
//zz
//   });
// });



$(function(){
  //画像ファイルプレビュー表示のイベント追加 fileを選択時に発火するイベントを登録
  $('form').on('change', 'input[type="file"]', function(e) {
    var file = e.target.files[0],
        reader = new FileReader(),
        $preview = $(".preview");
        t = this;

    // 画像ファイル以外の場合は何もしない
    if(file.type.indexOf("image") < 0){
      return false;
    }

    // ファイル読み込みが完了した際のイベント登録
    reader.onload = (function(file) {
      return function(e) {
        //既存のプレビューを削除
        $preview.empty();
        // .prevewの領域の中にロードした画像を表示するimageタグを追加
        $preview.append($('<img>').attr({
                  'src': e.target.result,
                  'class': 'preview',
                  'display':'block',
                  title: file.name
              }));
        $
      };
    })(file);

    reader.readAsDataURL(file);
  });
});


var button = document.getElementById('copyButton');
  button.addEventListener('click', function(){
    var yourCode = document.getElementById('copyTarget');
    var range = document.createRange();
    range.selectNode(yourCode);
    window.getSelection().addRange(range);
    document.execCommand('copy');
    alert('リンクをコピーしました');
  });

function copyToClipboard() {

           // コピー対象をJavaScript上で変数として定義する
           document.getElementById('copyTarget').select();
           document.execCommand('copy');

           // コピー対象のテキストを選択する


           // 選択しているテキストをクリップボードにコピーする

           // コピーをお知らせする
           alert("リンクをコピーしました");
           // target = document.getElementById("copy_msg");
           // target.innerHTML = "リンクをコピーしました";
       }



$(function() {

  // ①タブをクリックしたら発動
  $('.tab_box li').click(function() {

    // ②クリックされたタブの順番を変数に格納
    var index = $('.tab_box li').index(this);

    // ③クリック済みタブのデザインを設定したcssのクラスを一旦削除
    $('.tab_box li').removeClass('active');

    // ④クリックされたタブにクリック済みデザインを適用する
    $(this).addClass('active');

    // ⑤コンテンツを一旦非表示にし、クリックされた順番のコンテンツのみを表示
    $('.test').removeClass('show').eq(index).addClass('show');

  });
});

$(document).ready(function(){
  $('.menu_btn').on('click',function(){
    if( $(this).hasClass('active') ){
      $(this).removeClass('active');
      $('.header_sp').addClass('close').removeClass('open');
    }else {
      $(this).addClass('active');
      $('.header_sp').addClass('open').removeClass('close');
    }
  });
});


//ajax for likes
$(document).ready(function(){
  $('.button').on('click',function(){
    var post_id = $(this).attr('post_id');
    var condition = $(this).attr('condition');
    var firstname = $('#firstname'+post_id).val();
    var lastname = $('#lastname'+post_id).val();
    $.ajax({
      url : '/condition',
      type : 'POST',
      data : {
        firstname : firstname,
        lastname : lastname,
        id : post_id,
        condition : condition
        }
    })
     .done(function(data){
      if(data.condition == 'like'){
        $('.condition'+post_id).attr('condition','unlike').show();
        // $('.condition'+post_id).text('unlike').show();
           // $('.condition'+post_id).removeClass('fas');
           // $('.condition'+post_id).addClass('far');
        $('.condition'+post_id).css('opacity', '0.3');
        $('.count'+post_id).text(data.count).show();
      } else {
        $('.condition'+post_id).attr('condition','like').show();
           // $('.condition'+post_id).text('like').show();
           // $('.condition'+post_id).removeClass('far');
           // $('.condition'+post_id).addClass('fas');
        $('.condition'+post_id).css('opacity', '1.0');
        $('.count'+post_id).text(data.count).show();
      }
    });
      event.preventDefault();
  });
});

// TOPページへ戻る

$(function(){
  var topBtn = $('.page-top');
  topBtn.hide();
  // 100に到達したらボタンを出現させる。
  $(window).scroll(function(){
    if ($(this).scrollTop() > 100){
      topBtn.fadeIn();
    } else {
      topBtn.fadeOut();
    }
  });
  topBtn.click(function(){
    $('body,html').animate({
      scrollTop: 0
    },500);
  });

});
