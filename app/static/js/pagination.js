$(document).ready(function() {
        var offset = 3;
        $('#load-more-btn').on('click', function() {
            $.ajax({
                type: 'POST',
                url: '/load-more',
                data: { offset: offset },
                success: function(data) {
                    offset += data.length;
                    $('#item-list').append($.map(data, function(item) {
                        if (item) {
                            return `<h2>${item.name}</h2>
                                    <p>Цена: ${item.price} р.</p>
                                    <p>Описание: ${item.about}</p>
                                    <img src="${url_for('static', filename=item.img_link)}" alt="${item.name}">
                            `;
                        }
                        return '<h2>qqq</h2>';
                    }).join());
                }
            });
        });
    });
