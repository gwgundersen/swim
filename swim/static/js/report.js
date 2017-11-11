window.SWIM = {};

SWIM.visualize = function(stackedSeries, days, pieSeries) {
    SWIM.createStackedChart(stackedSeries, days);
    SWIM.createPieChart(pieSeries);
};


SWIM.createStackedChart = function(series, days) {
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
}