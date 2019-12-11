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
$(document).ready(function(){
  $('.slider_club').slick({
    infinite: true, //スライドのループ有効化
          dots:true, //ドットのナビゲーションを表示
          centerMode: true, //要素を中央寄せ
          centerPadding:'16%', //両サイドの見えている部分のサイズ
          autoplay:true, //自動再生
          autoplaySpeed:1400,
  });
  
  });

  $(document).ready(function(){
    $('.slider_food').slick({
      infinite: true, //スライドのループ有効化 //ドットのナビゲーションを表示
            centerMode: true, //要素を中央寄せ
            centerPadding:'18%', //両サイドの見えている部分のサイズ
            autoplay:true, //自動再生
            autoplaySpeed:1600,
    });
    
    });



$(function(){
  //ローディングエリアを取得
  var loading = $("#loading");
  //ローディングエリアを隠す処理
  var isHidden = function(){
    loading.fadeOut(1000); //1000ミリ秒かけてフェードアウト
  };
  //1000ミリ秒後にloadingFunc開始
  setTimeout(isHidden,1000);
});



$(function(){
  //画像ファイルプレビュー表示のイベント追加 fileを選択時に発火するイベントを登録
  $('form').on('change', 'input[type="file"]', function(e) {
    var file = e.target.files[0],
        reader = new FileReader(),
        $preview = $(".preview");
        t = this;
    if(file.type.indexOf("image") < 0){
      return false;
    }
    reader.onload = (function(file) {
      return function(e) {
        $preview.empty();
        $preview.append($('<img>').attr({
                  'src': e.target.result,
                  'class': 'preview',
                  'display':'block',
                  title: file.name
              }));
        $('#remove_image').remove();
      };
    })(file);
    reader.readAsDataURL(file);
  });
});



//
// function clipboadCopy(copyid){
//     var copytext = document.getElementById(copyid);
//     //この部分を追加
//     var range = document.createRange();
//     range.selectNode(copytext);
//     window.getSelection().addRange(range);
//     document.execCommand("copy");
// }



// コピーリンク
function copyToClipboard() {
           document.getElementById('copyTarget').select();
           document.execCommand('copy');
           alert("リンクをコピーしました");
}



// tab button
$(function() {
  $('.tab_box li').click(function() {
    var index = $('.tab_box li').index(this);
    $('.tab_box li').removeClass('active');
    $(this).addClass('active');
    $('.test').removeClass('show').eq(index).addClass('show');
  });
});


// menu function for SP
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

// timepicker
$(document).ready(function(){
  $('.timepicker').timepicker({
    timeFormat: 'HH:mm',
    interval: 10,
    minTime: '10',
    maxTime: '22:00',
    defaultTime: '11',
    startTime: '10:00',
    dynamic: false,
    dropdown: true,
    scrollbar: true
  });
});