@Gasoline.module "HeaderApp.List", (List, App, Backbone, Marionette, $, _) ->

    class List.Controller extends App.Controllers.Application

        initialize: ->
            @layout = @getLayoutView()

            @listenTo @layout, "show", =>
                @navLeftRegion()
                @navRightRegion()

            @show @layout

        navLeftRegion: ->
            navLeftView = @getNavLeftView()
            @layout.navLeftRegion.show navLeftView

        navRightRegion: ->
            navRightView = @getNavRightView()
            @layout.navRightRegion.show navRightView

        getNavLeftView: ->
            # collection of nav element
            collection = new Backbone.Collection
            collection.add [
                # { 'childView': List.NavCreate },
                { 'childView': List.NavSpaces },
                { 'childView': List.NavTests },
                { 'childView': List.NavSearch },
            ]

            new List.NavLeft
                collection: collection

        getNavRightView: ->
            # collection of nav element
            collection = new Backbone.Collection
            collection.add [
                { 'childView': List.NavUserMenu },
            ]

            new List.NavRight
                collection: collection

        getNavUserMenuView: ->
            new List.NavUserMenu

        getLayoutView: ->
            new List.LayoutView