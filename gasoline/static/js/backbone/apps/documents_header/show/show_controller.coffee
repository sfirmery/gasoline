@Gasoline.module "DocumentsHeaderApp.Show", (Show, App, Backbone, Marionette, $, _) ->

    class Show.Controller extends App.Controllers.Base

        initialize: (options) ->
            headerView = @getHeaderView options.mode, options.model
            @show headerView

        getHeaderView: (mode, model) ->
            new Show.Header
                mode: mode
                model: model
