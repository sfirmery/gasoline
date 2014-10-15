@Gasoline.module "WidgetSpacesApp", (WidgetSpacesApp, App, Backbone, Marionette, $, _) ->

    API =
        list: (region) ->
            new WidgetSpacesApp.List.Controller
                region: region
    
    App.commands.setHandler "show:widget:spaces", (region) ->
        API.list region
