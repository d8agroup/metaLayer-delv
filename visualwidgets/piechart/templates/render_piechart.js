var chart_data = {{ chart_data|safe }};

var chart_id = '{{ id }}';

var chart_{{ id }} = jQuery.jqplot
(
	chart_id,
	[chart_data],
	{
		seriesColors: [ "#D80000", "#F06000", "#D89000", "#780000", "F00000" ],
		seriesDefaults: 
		{
			renderer: jQuery.jqplot.PieRenderer,
			rendererOptions: 
			{ 
				showDataLabels: true,
				dataLabels:'label'
			}
		},
		legend: 
		{ 
			show:false,
		},
		grid: 
		{ 
			shadow:false,
			background:'transparent',
			borderWidth:0,
            borderColor: 'transparent' 
		},
	}
);
