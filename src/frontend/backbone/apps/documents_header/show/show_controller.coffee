@Gasoline.module "DocumentsHeaderApp.Show", (Show, App, Backbone, Marionette, $, _) ->

    class Show.Controller extends App.Controllers.Application

        initialize: (options) ->
            @setMainView @headerView options.mode, options.model

        headerView: (mode, document) ->
            @getHeaderView mode, document

        getHeaderView: (mode, model) ->
            new Show.Header
                mode: mode
                model: model
