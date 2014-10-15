@Gasoline.module "WidgetActivityStreamApp", (WidgetActivityStreamApp, App, Backbone, Marionette, $, _) ->

    API =
        list: (region) ->
            new WidgetActivityStreamApp.List.Controller
                region: region
    
    App.commands.setHandler "show:widget:activitystream", (region) ->
        API.list region
