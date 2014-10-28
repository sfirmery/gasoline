@Gasoline.module "UsersApp.Edit", (Edit, App, Backbone, Marionette, $, _) ->

    class Edit.Controller extends App.Controllers.Application

        initialize: (options) ->
            { users, user } = options
            user ?= App.request "new:user:entity"

            console.log "user new", user.isNew()

            userView = @getUserView users, user

            form = App.request "form:component", userView,
                proxy: "dialog"
                proxyLayout: true
                onFormCancel: => @region.empty()
                onFormSuccess: => @region.empty()

            @show form

        getUserView: (users, user) ->
            new Edit.User
                collection: users
                model: user
