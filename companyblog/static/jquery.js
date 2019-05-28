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
