var values = {{ values|safe }};

var names = {{ names|safe }};

var chart_id = '{{ id }}';

var chart_{{ id }} = jQuery.jqplot
(
	chart_id,
	[values],
	{
		seriesDefaults: 
		{
			renderer: jQuery.jqplot.BarRenderer,
			rendererOptions: { fillToZero: true }
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
		axes:
		{
			xaxis: 
			{
            	renderer: $.jqplot.CategoryAxisRenderer,
            	ticks: names
			},
			yaxis:
			{
				showLabel:false,
				tickOptions: { show:false }
			}
		}
	}
);
