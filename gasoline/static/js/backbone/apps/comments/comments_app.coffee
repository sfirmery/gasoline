@Gasoline.module "CommentsApp", (CommentsApp, App, Backbone, Marionette, $, _) ->
        
    API =
        list: (model, region) ->
            new CommentsApp.List.Controller
                model: model
                region: region

    App.commands.setHandler "show:comments", (model, region) ->
        API.list model, region
