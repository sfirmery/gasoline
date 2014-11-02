@Gasoline.module "PeopleApp", (PeopleApp, App, Backbone, Marionette, $, _) ->

    class PeopleApp.Router extends Marionette.AppRouter
        appRoutes:
            "people": "list"
            "people/:user": "show"
        
    API =
        list: ->
            new PeopleApp.List.Controller

        show: (user) ->
            new PeopleApp.Show.Controller
                user: user

        edit: (user) ->
            new PeopleApp.Edit.Controller 
                region: App.dialogRegion
                user: user

        newUser: (people) ->
            new PeopleApp.Edit.Controller
                region: App.dialogRegion
                people: people

    App.vent.on "edit:user:clicked", (user) ->
        API.edit user

    App.vent.on "new:user:clicked", (people) ->
        API.newUser people

    App.addInitializer ->
        new PeopleApp.Router
            controller: API
