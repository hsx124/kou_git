var PlotUtil = {
    plot : function(id, values, options) {
        $.jqplot(id, [ values ], options);
    },

    plotBarRenderer : function(id, values) {
        $.jqplot(id, [ values ], {
            seriesDefaults : {
                renderer : jQuery.jqplot.BarRenderer,
                rendererOptions : {
                    barDirection : "horizontal"
                },
                pointLabels : {
                    show : true,
                    location : 'e',
                    escapeHTML : false,
                    formatString : "<b>%'d</b>"
                }
            },
            axes : {
                yaxis : {
                    renderer : $.jqplot.CategoryAxisRenderer,
                    labelOptions : {
                        fontSize : '20pt',
                    }
                },
                xaxis : {
                    tickOptions : {
                        formatString : "<b>%'d</b>"
                    }
                }
            }
        });
    },
};