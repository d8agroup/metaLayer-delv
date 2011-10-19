function class_inputwidget(collection_id, container)
{
	this.container = container;
	
	this.collection_id = collection_id;
	
	this.render = function()
	{
		var render_shell_url = '/inputwidget/render';
		var render_input_summary_url = '/inputwidget/input/rendersummary'
		var get_config_url = '/config/get';

		$.get 
		(
			render_shell_url,
			function(template)
			{
				var shell = $(template);
				$.get
				(
					get_config_url,
					function(config)
					{
						if(this.collection_id in config.collections)
						{
							collection_config = config.collections[this.collection_id]
							for(var x=0; x<collection_config.input_widgets.length; x++)
							{
								var input = new class_input(collection_config.input_widgets[x]);
								$.get
								(
									render_input_summary_url + "?collection_id=" + this.collection_id + "&input_id=" + input.id + "&title=" + input.get_title() + "&type=" + input.type,
									function(input_summary_template)
									{
										shell.find('.input_widget_inputs').append(input_summary_template);
									}
								)
							}
						}
					}
				)
				container.append(shell);
			}
		)
	}
}

function class_input(input)
{
	this.id = input.id;
	
	this.type = input.type;
	
	this.config = input.config;
	
	this.get_title = function()
	{
		switch(this.type)
		{
			case "twittersearch": return 'Twitter Search: ' + this.config.keywords;
		}
	}
}