@Gasoline.module "DocumentsHeaderApp", (DocumentsHeaderApp, App, Backbone, Marionette, $, _) ->

    API =
        list: (mode, model, region) ->
            new DocumentsHeaderApp.Show.Controller
                mode: mode
                model: model
                region: region
    
    App.commands.setHandler "show:documents:header", (mode, model, region) ->
        API.list mode, model, region
