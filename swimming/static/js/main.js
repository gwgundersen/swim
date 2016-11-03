$(function() {

    sortable('ul#todo, ul#queued, ul#done', {
        connectWith: '.connected'
    })[0].addEventListener('sortupdate', save_wins_status);

    /* Save new ordering for small wins.
     */
    function save_wins_status(evt) {
        console.log('wins changed');
        var updates = [];
        $('#index-page ul').each(function(i, ul) {
            $(ul).find('li').each(function(i, li) {
                updates.push({
                    id: $(li).find('input').attr('name'),
                    status: $(ul).attr('id'),
                    rank: i
                });
            });
        });

        $.ajax({
            url: '/swimming/win/update_rank',
            type: 'POST',
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
                updates: updates
            })
        })
    }

    $('#wins-completed-page table').DataTable({
        bSort: false
    });

});
