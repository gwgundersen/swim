$(function() {

    if ($('#index-page').length) {
        sortable('ul#todo, ul#queued, ul#done', {
            connectWith: '.connected'
        })[0].addEventListener('sortupdate', save_tasks_updates);
    }

    /* Save new properties for small tasks.
     */
    function save_tasks_updates(evt) {
        var updates = [];
        $('#index-page ul').each(function(i, ul) {
            $(ul).find('li').each(function(i, li) {
                updates.push({
                    id: $(li).find('input').attr('name'),
                    status: $(ul).attr('id'),
                    rank: i
                });
            });

            updateStyles(ul);
        });

        $.ajax({
            url: '/swim/task/update_rank',
            type: 'POST',
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
                updates: updates
            })
        })
    }

    function updateStyles(ul) {
        $(ul).find('li').removeClass('last').last().addClass('last');
    }

});
