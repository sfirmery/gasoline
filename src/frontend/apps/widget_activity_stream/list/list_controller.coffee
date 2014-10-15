@Gasoline.module "WidgetActivityStreamApp.List", (List, App, Backbone, Marionette, $, _) ->

    class List.Controller extends App.Controllers.Base

        initialize: ->
            activities = App.request "activities:entities"

            App.execute "when:fetched", activities, =>
                @activityStreamView activities

        activityStreamView: (activities) ->
            activityStreamView = @getActivityStreamView activities
            @show activityStreamView
        
        getActivityStreamView: (activities) ->
            new List.Activities
                collection: activities
