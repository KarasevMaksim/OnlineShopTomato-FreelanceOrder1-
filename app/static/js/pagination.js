$(document).ready(function() {
    $('#update-button').click(function() {
        $.ajax({
            type: 'POST',
            url: '/update',
            success: function(response) {
                // Добавляем содержимое в конец элемента с id 'item-list'
                $('#item-list').append(response);
            },
            error: function() {
                alert('An error occurred');
            }
        });
    });
});
