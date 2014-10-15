@Gasoline.module "DashboardApp.Show", (Show, App, Backbone, Marionette, $, _) ->

    class Show.Controller extends App.Controllers.Base

        initialize: ->
            @layout = @getLayoutView()

            @listenTo @layout, "show", =>
                @showWidgetSpaces()
                @showWidgetActivityStream()

            @show @layout
        
        showWidgetSpaces: ->
            App.execute "show:widget:spaces", @layout.spacesListRegion

        showWidgetActivityStream: ->
            App.execute "show:widget:activitystream", @layout.activityStreamRegion

        getLayoutView: ->
            new Show.LayoutView