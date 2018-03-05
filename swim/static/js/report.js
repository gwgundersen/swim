window.SWIM = {};

SWIM.colorMap = {
    'research'     : '#3cb44b',
    'coursework'   : '#ffe119',
    'development'  : '#0082c8',
    'side_projects': '#f58231',
    'yak_shaving'  : '#911eb4',
    'personal'     : '#46f0f0',
    'pti'          : '#f032e6',
    'teaching'     : '#d2f53c',
    'ka_math'      : '#fabebe',
    'rest'         : '#008080',
    'hunt'         : '#e6beff',
    'health'       : '#aa6e28'
};

SWIM.visualize = function(stackedSeries, days, pieSeries) {
    SWIM.createStackedChart(stackedSeries, days);
    SWIM.createPieChart(pieSeries);
};


SWIM.createStackedChart = function(series, days) {
    series = assignColors(series);
    Highcharts.chart('stacked-chart', {
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
                formatter: function () {
                    var dayAsInt = new Date(this.value).getDay(),
                        dayAsName = [
                            'Mon', 'Tue', 'Wed',
                            'Thu', 'Fri', 'Sat', 'Sun'][dayAsInt],
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
}


SWIM.createPieChart = function(series) {
    series = assignColors(series);
    Highcharts.chart('pie-chart', {
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: 'Time spent by category'
        },
        tooltip: {
            formatter: function() {
                var p = this.point;
                return '<strong>' + p.name + ':</strong> '
                    + p.y.toFixed(1) + ' hrs, '
                    + p.percentage.toFixed(1) + '%';
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: false
                },
                showInLegend: true
            }
        },
        series: [{
            name: 'Labels',
            colorByPoint: true,
            data: series
        }]
    });
};

function assignColors(series) {
    series.forEach(function(obj, i) {
        obj.color = SWIM.colorMap[obj.name];
    });
    return series;
}