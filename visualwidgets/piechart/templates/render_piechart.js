var chart_data = {{ chart_data|safe }};

var chart_id = '{{ id }}';

var chart_{{ id }} = jQuery.jqplot
(
	chart_id,
	[chart_data],
	{
		seriesDefaults: 
		{
			renderer: jQuery.jqplot.PieRenderer,
			rendererOptions: 
			{ 
				showDataLabels: true,
				dataLabels:'label'
			}
		}
	}
);
