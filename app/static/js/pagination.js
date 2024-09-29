$(document).ready(function() {
    var offset = 9;
    $('#load-more-btn').on('click', function() {
      $.ajax({
        type: 'POST',
        url: '/load-more',
        data: { offset: offset },
        success: function(html) {
          $('#item-list').append(html);
          offset += 9;
        }
      });
    });
  });