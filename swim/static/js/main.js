$(function() {

    var taskBeingEdited = false;

    if ($('#index-page').length) {
        sortable('ul#todo, ul#queued, ul#done', {
            connectWith: '.connected'
        })[0].addEventListener('sortupdate', saveTasksUpdates);

        $('ul li').dblclick(function() {
            if (taskBeingEdited) {
                return;
            }
            taskBeingEdited = true;
            var $currentEl = $(this).find('span'),
                description = $currentEl.html();
            updateVal($currentEl, description);
        });
    }

    /* Save new properties for small tasks.
     */
    function saveTasksUpdates() {
        var updates = [];
        $('#index-page ul').each(function(i, ul) {
            $(ul).find('li').each(function(i, li) {
                updates.push({
                    id: $(li).find('input').attr('name'),
                    description: $(li).find('span').text(),
                    status: $(ul).attr('id'),
                    rank: i
                });
            });
        });

        $.ajax({
            url: '/swim/task/update_via_json',
            type: 'POST',
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
                updates: updates
            })
        })
    }

    function updateVal($currentEl, description) {
        $currentEl.html('<input class="task-being-edited" type="text" value="' + description + '" />');
        var $task = $(".task-being-edited");
        $task
            .focus()
            .keyup(function (event) {
                if (event.keyCode == 13) {
                    $currentEl.html($task.val().trim());
                }
            });

        $(document).click(function(evt) {
            if ($task.length && !$(evt.target).hasClass("task-being-edited")) {
                $currentEl.html($task.val().trim());
                taskBeingEdited = false;
                saveTasksUpdates();
            }
        });
    }

});
