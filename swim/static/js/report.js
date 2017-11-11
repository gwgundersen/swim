window.SWIM = {};

window.SWIM.visualize = function (series, days) {
    Highcharts.chart('visualization', {
        chart: {
            type: 'area'
        },
        title: {
            text: 'Activity per day'
        },
        xAxis: {
            categories: days,
            tickmarkPlacement: 'on',
            title: {
                enabled: false
            },
            labels: {
                formatter: function() {
                    var dayAsInt = new Date(this.value).getDay(),
                        dayAsName = [
                            'Sun', 'Mon', 'Tue', 'Wed',
                            'Thu', 'Fri', 'Sat'][dayAsInt],
                        date,
                        parts;
                    parts = this.value.split('-');
                    date = parts[1] + '/' + parts[2];
                    return dayAsName + ' (' + date + ')';
                }
            }
        },
        yAxis: {
            title: {
                text: 'Hours'
            }
        },
        tooltip: {
            split: true,
            valueSuffix: ' hours'
        },
        plotOptions: {
            area: {
                stacking: 'normal',
                lineColor: '#666666',
                lineWidth: 1,
                marker: {
                    lineWidth: 1,
                    lineColor: '#666666'
                }
            }
        },
        series: series
    });
};