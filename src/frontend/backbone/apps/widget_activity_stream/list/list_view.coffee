@Gasoline.module "WidgetActivityStreamApp.List", (List, App, Backbone, Marionette, $, _) ->
    
    class List.Activity extends App.Views.ItemView
        template: "widget_activity_stream/list/_activity"

    class List.Activities extends App.Views.CompositeView
        template: "widget_activity_stream/list/_activity_stream"
        childView: List.Activity
