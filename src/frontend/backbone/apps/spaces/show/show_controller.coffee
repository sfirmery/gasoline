@Gasoline.module "SpacesApp.Show", (Show, App, Backbone, Marionette, $, _) ->

    class Show.Controller extends App.Controllers.Application

        initialize: (options) ->
            space = App.request "spaces:entity", options.space

            App.execute "when:fetched", space, =>
                @layout = @getLayoutView()

                @listenTo @layout, "show", =>
                    @spaceRegion space

                @show @layout

        spaceRegion: (space) ->
            spaceView = @getSpaceView space
            @show spaceView, region: @layout.spaceRegion

        showHeader: (space) ->
            App.execute "show:spaces:header", "show", space, @layout.spaceHeaderRegion

        getSpaceView: (space) ->
            new Show.Space
                model: space

        getLayoutView: ->
            new Show.LayoutView
