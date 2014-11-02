@Gasoline.module "CommentsApp", (CommentsApp, App, Backbone, Marionette, $, _) ->
        
    API =
        list: (model) ->
            new CommentsApp.List.Controller
                model: model

    App.reqres.setHandler "list:comments", (model) ->
        throw new Error "Comments List requires a model to be passed in" if not model
        API.list model
