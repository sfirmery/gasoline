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

		edit: (user, model) ->
			new UsersApp.Edit.Controller 
				user: user
				model: model
			
	App.addInitializer ->
		new UsersApp.Router
			controller: API
	
	App.vent.on "user:saved", (model) ->
		API.show null, model
		App.navigate "users/#{model.id}"
