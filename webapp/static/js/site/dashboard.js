/***********************************************************************************************************************
DASHBOARD - widgets panel
***********************************************************************************************************************/
(function( $ )
{
    var methods =
    {
        init:function(data)
        {
            var widgets = data.widgets;
            this.children().remove();
            var empty_widget_panel_html = $("<div id='widget_panel'></div>");

            //TODO: this is a temp hack
            <div class='widget data_point_widget'><p class='hidden type'>twitter</p><p class='hidden sub_type'>search</p>twitter</div>
            var twitter_widget = $('<div class="data_point_widget">twitter</div>');
            twitter_widget.data
            (
                'data_point',
                {
                    type:'twitter',
                    sub_type:'search',
                    short_display_name:'Twitter Search',
                    full_display_name:'Search Twitter',
                    configured_display_name:'Twitter Search for XYZ',
                    instructions:'To start searching twitter you will need to choose the keyword(s) you want to search for.',
                    image:'http://www.exacta.com/sites/default/files/pictures/twitter-logo.png',
                    configured:false,
                    elements:[
                        {name:'keywords', display_name:'Keywords', help:'Enter the keywords you want to search for', type:'text', validation:null, value:'' }
                    ]
                }
            );
            empty_widget_panel_html.append(twitter_widget);

            this.html(empty_widget_panel_html);
            this.dashboard_widget_panel('apply_widget_draggable');
            return this;
        },
        apply_widget_draggable:function()
        {
            this.find('.data_point_widget').draggable
            (
                {
                    revert:true,
                    helper:"clone",
                    start:function()
                    {
                        $('#collections').dashboard_collections_panel('data_point_start_dragging');
                    },
                    stop:function()
                    {
                        $('#collections').dashboard_collections_panel('data_point_stop_dragging');
                    }
                }
            );
        }
    }

    $.fn.dashboard_widget_panel = function( method ){
        if ( methods[method] ) return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        else if ( typeof method === 'object' || ! method ) return methods.init.apply( this, arguments );
        else $.error( 'Method ' +  method + ' does not exist on jQuery.tooltip' );}
})( jQuery );

/***********************************************************************************************************************
DASHBOARD - collections panel
***********************************************************************************************************************/
(function( $ )
{
    var methods =
    {
        init:function(data)
        {
            this.children().remove();
            var collections = data.collections;
            var collection_class = 'collections_' + collections.length;
            for (collection in collections)
            {
                var collection_container_html = '<div class="collection_container ' + collection_class + '"></div>';
                var collection_container = $(collection_container_html).dashboard_collection({ collection:collections });
                this.append(collection_container);
            }
            return this;
        },
        data_point_start_dragging:function()
        {
            this.find('.collection_container').dashboard_collection('data_point_start_dragging');
        },
        data_point_stop_dragging:function()
        {
            this.find('.collection_container').dashboard_collection('data_point_stop_dragging');
        }
    }

    $.fn.dashboard_collections_panel = function( method ){
        if ( methods[method] ) return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        else if ( typeof method === 'object' || ! method ) return methods.init.apply( this, arguments );
        else $.error( 'Method ' +  method + ' does not exist on jQuery.tooltip' );}
})( jQuery );


/***********************************************************************************************************************
DASHBOARD
***********************************************************************************************************************/
(function( $ )
{
    var methods =
    {
        init:function(data)
        {
            var dashboard = data.dashboard;
            this.find('#widgets').dashboard_widget_panel({widgets:dashboard.widgets});
            this.find('#collections').dashboard_collections_panel({'collections':dashboard.collections})
        }
    }

    $.fn.dashboard = function( method ) {
        if ( methods[method] ) return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        else if ( typeof method === 'object' || ! method ) return methods.init.apply( this, arguments );
        else $.error( 'Method ' +  method + ' does not exist on jQuery.tooltip' ); }
})( jQuery );