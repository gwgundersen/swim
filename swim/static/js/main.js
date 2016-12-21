$(function() {

    var taskBeingEdited = false;

    if ($('#index-page').length) {
        sortable('ul#todo, ul#queued, ul#done', {
            connectWith: '.connected'
        })[0].addEventListener('sortupdate', saveTasksUpdates);

        $('ul li span').dblclick(function() {
            if (taskBeingEdited) {
                return;
            }
            taskBeingEdited = true;
            var $currentEl = $(this),
                value = $currentEl.html();
            updateVal($currentEl, value);
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
                    description: $(li).find('.description').text(),
                    duration: $(li).find('.duration').text(),
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
            }),
            error: function(data) {
                alert(JSON.parse(data.responseText).message);
            }
        })
    }

    function updateVal($currentEl, value) {
        $currentEl.html('<input class="task-being-edited" type="text" value="' + value + '" />');
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
