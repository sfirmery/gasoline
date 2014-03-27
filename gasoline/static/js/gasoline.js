$(document).ready(function() {
  $("abbr.timeago").timeago();
});

$('#search_input').find('input').on('focus',function(){
    $(this).animate({width: '300px'},200);
    $("#search_results").animate({width: '300px'},200).show();
  }).on('focusout', function() {
    $(this).animate({width: '180px'},200);
    $("#search_results").animate({width: '180px'},200).hide();
});

var search_timer = 0;
var search_in_progress = 0;
var search_last_keyup_value = '';
$('#search_input').find('input').keyup(function() {
  if (search_timer != null) {
    clearTimeout(search_timer);
  }
  search_timer = setTimeout(quick_search, 200);
});

function quick_search() {
  var searchbox = $('#search_input').find('input').val();
  var dataString = 'query='+ searchbox;
  if(searchbox != '' && search_last_keyup_value != searchbox){
    search_in_progress++;
    $("#search_button").removeClass('fa-search');
    $("#search_button").addClass('fa-spinner fa-spin');
    $.ajax({
      type: "GET",
      url: "/api/quick_search",
      data: dataString,
      cache: false,
      success: function(data) {
        var html = '';
        for (var i=0;i<data.results.list.length;i++) {
          result = data.results.list[i];
          html += '<li class="search_results">';
          html += '<a href="'+result.url+'">'
          html += result.title
          html += ' - '+result.space
          html += '</a>'
          html += '</li>';
        }
        html += '';
        $("#search_results").html(html);
      },
      complete: function() {
        search_in_progress--;
        if (search_in_progress <= 0) {
          $("#search_button").removeClass('fa-spinner fa-spin');
          $("#search_button").addClass('fa-search');
        }
      }
    });
  }
  search_last_keyup_value = searchbox;
  return false;
}