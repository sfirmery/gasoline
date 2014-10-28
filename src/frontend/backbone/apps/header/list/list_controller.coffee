@Gasoline.module "HeaderApp.List", (List, App, Backbone, Marionette, $, _) ->

    class List.Controller extends App.Controllers.Application

        initialize: ->
            @layout = @getLayoutView()

            @listenTo @layout, "show", =>
                @navRegion()

            @show @layout

        navRegion: (document) ->
            navView = @getNavView()
            @layout.navRegion.show navView

        getNavView: ->
            new List.Nav

        getLayoutView: ->
            new List.LayoutView