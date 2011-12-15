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
            var empty_widget_panel_html = "<div id='widget_panel'></div>";
            this.html(empty_widget_panel_html);
            return this;
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
        }
    }

    $.fn.dashboard_collections_panel = function( method ){
        if ( methods[method] ) return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        else if ( typeof method === 'object' || ! method ) return methods.init.apply( this, arguments );
        else $.error( 'Method ' +  method + ' does not exist on jQuery.tooltip' );}
})( jQuery );

/** DASHBOARD - collection ********************************************************************************************/
(function( $ )
{
    var methods =
    {
        init:function(data)
        {
            var collection = data.collection;
            if (collection.data_points == null)
            {
                var empty_collection_html = "<div class='empty_collection'><p>Drag & Drop Data</p></div>";
                this.html(empty_collection_html);
            }
            else
            {

            }
            return this;
        }
    };

    $.fn.dashboard_collection = function( method ){
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