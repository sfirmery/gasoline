@Gasoline.module "UsersApp", (UsersApp, App, Backbone, Marionette, $, _) ->

  class UsersApp.Router extends Marionette.AppRouter
    appRoutes:
      "users": "list"
      "users/:user": "show"
      "users/:user/edit": "edit"
    
  API =
    list: ->
      new UsersApp.List.Controller

    show: (user, model) ->
      new UsersApp.Show.Controller
        user: user
        model: model

    edit: (user) ->
      new UsersApp.Edit.Controller 
        region: App.dialogRegion
        user: user

    newUser: (users) ->
      new UsersApp.Edit.Controller
        region: App.dialogRegion
        users: users

  App.vent.on "user:saved", (user) ->
    API.show null, user
    App.navigate "users/#{user.id}"

  App.vent.on "user:created", (member) ->
    # App.navigate Routes.edit_crew_path(member.id)
    API.edit member.id, member

  App.vent.on "user:updated", (crew) ->
    # App.navigate Routes.crew_index_path()
    API.list()

  App.vent.on "edit:user:clicked", (user) ->
    API.edit user

  App.vent.on "new:user:clicked", (users) ->
    API.newUser users

  App.addInitializer ->
    new UsersApp.Router
      controller: API
