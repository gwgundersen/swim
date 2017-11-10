$(function() {

    if ($('#index-page').length) {
        saveTasksUpdates();
        highlightFirstItem();
        setupTimer();
        sortable('ul#todo, ul#queued, ul#done', {
            connectWith: '.connected'
        })[0].addEventListener('sortupdate', saveTasksUpdates);
    }

    /* Save new properties for small tasks.
     */
    function saveTasksUpdates() {
        var updates = [];
        $('#index-page ul.connected').each(function(i, ul) {
            $(ul).find('li').each(function(i, li) {
                updates.push({
                    id: $(li).attr('name'),
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

        debugger;
        updateTimesAndPercentages(updates);
        highlightFirstItem();
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

    function setupTimer() {
        var startTime = window.localStorage.getItem('swim-start-time'),
            $clock = $('#timer span'),
            $startStop = $('#timer #start-btn'),
            CHECK_EVERY = 1000,
            started = false,
            timer;

        $startStop.click(function() {
            if (started) {
                $startStop.html('Start');
                window.localStorage.removeItem('swim-start-time');
                clearInterval(timer);
            } else {
                $startStop.html('Stop');
                startTime = startTime ? startTime : Date.now();
                window.localStorage.setItem('swim-start-time', startTime);
                timer = setInterval(function() {
                    $clock.html("Min: " + getMinutesElapsed(startTime));
                }, CHECK_EVERY);
            }
            started = !started;
        });

        // LocalStorage saves "undefined" as a string, not a JS value.
        if (startTime) {
            $startStop.trigger('click');
        }
    }

    function getMinutesElapsed(startTime) {
        var delta = Date.now() - parseInt(startTime);
        // Milliseconds to minutes.
        return Math.floor(delta / 60000);
    }

    function highlightFirstItem() {
        $('ul#todo').find('li').removeClass('first');
        $('ul#todo').find('li').first().addClass('first');
    }

    $('#completed-tasks-table').DataTable({
        order: [[ 2, 'desc' ]],
        paging: false
    });

    $('#upcoming-tasks-table').DataTable({
        order: [[ 3, 'asc' ]],
        paging: false
    });
});
