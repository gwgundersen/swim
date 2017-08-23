$(function() {

    var taskBeingEdited = false;

    if ($('#index-page').length) {
        saveTasksUpdates();
        highlightFirstItem();

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
        $('#index-page ul.connected').each(function(i, ul) {
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

        updateTimesAndPercentages(updates);
        highlightFirstItem();
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

    function updateTimesAndPercentages(updates) {
        var times = {
            todo: {
                total: 0,
                labels: {}
            },
            queued: {
                total: 0,
                labels: {}
            },
            done: {
                total: 0,
                labels: {}
            }
        };
        $.each(updates, function(i, obj) {
            var time = parseInt(obj.duration),
                label = obj.labels.split(',')[0],
                status = obj.status;
            times[status].total += time;
            if (typeof times[status].labels[label] === 'undefined') {
                times[status].labels[label] = 0
            }
            times[status].labels[label] += time;
        });
        // This tracks the status column with the most labels so that we can
        // create blank list items for columns with fewer labels. This ensures
        // the columns looks like they start at the same height.
        var maxNLables = Math.max(
            Object.keys(times.todo.labels).length,
            Object.keys(times.queued.labels).length,
            Object.keys(times.done.labels).length
        );

        $.each(times, function(status, obj) {
            var hours = (obj.total / 60.0).toFixed(2) + " hrs",
                $list = $('#' + status).parent().find('ul.label-pcts'),
                nItems = 0;
            $('#' + status).parent().find('.total-time').text(hours);
            $list.empty();
            $.each(obj.labels, function(label, duration) {
                var pct = Math.round(duration / obj.total * 100),
                    text = label + ": " + pct + '%';
                $list.append('<li>' + text + '</li>');
                nItems += 1;
            });
            for (var i = 0; i < maxNLables - nItems; i++) {
                $list.append('<li>&nbsp;</li>');
            }
        });
    }

    function highlightFirstItem() {
        $('ul#todo').find('li').removeClass('first');
        $('ul#todo').find('li').first().addClass('first');
    }

    $('table').DataTable();
});
