@Gasoline.module "SpacesApp.Show", (Show, App, Backbone, Marionette, $, _) ->

    class Show.Controller extends App.Controllers.Base

        initialize: (options) ->
            @layout = @getLayoutView()

            # render region when render layout
            @listenTo @layout, "show", =>
                @showHeader space
                @spaceView space

            # @space = options.space or options.model.id
            if options.space != null
                space = App.request "spaces:entity", options.space

                App.execute "when:fetched", space, =>
                    @show @layout
            else
                space = options.model
                @show @layout

        spaceView: (space) ->
            spaceView = @getSpaceView space
            @show spaceView, region: @layout.spaceRegion

        showHeader: (space) ->
            App.execute "show:spaces:header", "show", space, @layout.spaceHeaderRegion

        getSpaceView: (space) ->
            new Show.Space
                model: space

        getLayoutView: ->
            new Show.LayoutView
