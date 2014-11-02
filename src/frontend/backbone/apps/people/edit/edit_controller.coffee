@Gasoline.module "PeopleApp.Edit", (Edit, App, Backbone, Marionette, $, _) ->

    class Edit.Controller extends App.Controllers.Application

        initialize: (options) ->
            { people, user } = options
            user ?= App.request "new:user:entity"

            userView = @getUserView people, user

            form = App.request "form:component", userView,
                proxy: "dialog"
                proxyLayout: true
                onFormCancel: => @region.empty()
                onFormSuccess: => @region.empty()

            @show form

        getUserView: (people, user) ->
            new Edit.User
                collection: people
                model: user
