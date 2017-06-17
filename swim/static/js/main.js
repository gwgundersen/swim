$(function() {

    var taskBeingEdited = false;

    if ($('#index-page').length) {
        saveTasksUpdates();

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
                    labels: $(li).find('.labels').text(),
                    status: $(ul).attr('id'),
                    rank: i
                });
            });
        });

        $.ajax({
            url: '/task/update_via_json',
            type: 'POST',
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
                updates: updates
            }),
            error: function(data) {
                alert(JSON.parse(data.responseText).message);
            }
        });

        updateTotalTimes(updates);
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

    function updateTotalTimes(updates) {
        var times = {
            'todo': 0,
            'queued': 0,
            'done': 0
        };
        $.each(updates, function(i, obj) {
            times[obj.status] += parseInt(obj.duration);
        });
        $.each(times, function(key, val) {
            var hours = (val / 60.0).toFixed(2) + " hrs";
            $('#' + key).parent().find('.total-time').text(hours);
        });
    }

    $('table').DataTable();

});
