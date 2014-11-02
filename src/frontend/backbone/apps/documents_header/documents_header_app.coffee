@Gasoline.module "DocumentsHeaderApp", (DocumentsHeaderApp, App, Backbone, Marionette, $, _) ->

    API =
        list: (mode, model) ->
            new DocumentsHeaderApp.Show.Controller
                mode: mode
                model: model
    
    App.reqres.setHandler "documents:header", (mode, model) ->
        throw new Error "Tags List requires a mode to be passed in" if not mode
        throw new Error "Tags List requires a model to be passed in" if not model
        API.list mode, model
