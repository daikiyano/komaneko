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
