@Gasoline.module "Entities", (Entities, App, Backbone, Marionette, $, _) ->

    baseUrl = "/api/v1/activity"

    class Entities.Activity extends Entities.Model
        urlRoot: baseUrl

    class Entities.ActivitiesCollection extends Entities.Collection
        model: Entities.Activity
        url: baseUrl

    API =
        getActivities: (params = {}) ->
            _.defaults params, {}

            activities = new Entities.ActivitiesCollection
            activities.fetch
                data: params
            activities

    # request list of activities
    App.reqres.setHandler "activities:entities", ->
        API.getActivities()
