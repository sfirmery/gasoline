@Gasoline.module "DocumentsHeaderApp.Show", (Show, App, Backbone, Marionette, $, _) ->

    class Show.Controller extends App.Controllers.Base

        initialize: (options) ->
            @headerView options.mode, options.model

        headerView: (mode, document) ->
            headerView = @getHeaderView mode, document
            @show headerView

        getHeaderView: (mode, model) ->
            new Show.Header
                mode: mode
                model: model
