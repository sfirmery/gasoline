@Gasoline.module "DocumentsApp.Links", (Links, App, Backbone, Marionette, $, _) ->

    class Links.Controller extends App.Controllers.Application

        initialize: (options) ->
            {model} = options

            linksView = @getLinksView model
            @show linksView
            Backbone.Syphon.deserialize linksView, model.toJSON()

        getLinksView: (model) ->
            new Links.View
                model: model
