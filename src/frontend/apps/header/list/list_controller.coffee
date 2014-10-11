@Gasoline.module "HeaderApp.List", (List, App, Backbone, Marionette, $, _) ->

    class List.Controller extends App.Controllers.Base

        initialize: ->
            @layout = @getLayoutView()

            @listenTo @layout, "show", =>
                @navView()

            @show @layout

        navView: (document) ->
            navView = @getNavView()
            @show navView, region: @layout.navRegion

        getNavView: ->
            new List.Nav

        getLayoutView: ->
            new List.LayoutView