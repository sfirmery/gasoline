@Gasoline.module "CommentsApp", (CommentsApp, App, Backbone, Marionette, $, _) ->
        
    API =
        edit: (model) ->
            new CommentsApp.Edit.Comment
                model: model

        list: (model, region) ->
            new CommentsApp.List.Controller
                model: model
                region: region

    App.commands.setHandler "show:comments", (model, region) ->
        API.list model, region
