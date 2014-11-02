@Gasoline.module "SpacesApp", (SpacesApp, App, Backbone, Marionette, $, _) ->

    class SpacesApp.Router extends Marionette.AppRouter
        appRoutes:
            "spaces": "list"
            "spaces/:space": "show"
        
    API =
        list: ->
            new SpacesApp.List.Controller

        show: (space) ->
            new SpacesApp.Show.Controller
                space: space

        edit: (space) ->
            new SpacesApp.Edit.Controller
                region: App.dialogRegion
                space: space

        newSpace: (spaces) ->
            new SpacesApp.Edit.Controller
                region: App.dialogRegion
                spaces: spaces

    App.vent.on "edit:space:clicked", (space) ->
        API.edit space

    App.vent.on "new:space:clicked", (spaces) ->
        API.newSpace spaces

    App.addInitializer ->
        new SpacesApp.Router
            controller: API
