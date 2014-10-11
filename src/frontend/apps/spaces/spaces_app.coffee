@Gasoline.module "SpacesApp", (SpacesApp, App, Backbone, Marionette, $, _) ->

	class SpacesApp.Router extends Marionette.AppRouter
		appRoutes:
			"spaces": "list"
			"spaces/:space": "show"
			"spaces/:space/edit": "edit"
		
	API =
		list: ->
			new SpacesApp.List.Controller

		show: (space, model) ->
			new SpacesApp.Show.Controller
				space: space
				model: model

		edit: (space, model) ->
			new SpacesApp.Edit.Controller
				space: space
				model: model

	App.addInitializer ->
		new SpacesApp.Router
			controller: API

	App.vent.on "space:saved", (model) ->
        App.vent.trigger "show:space", model

	App.vent.on "edit:space", (model) ->
		API.edit null, model
		App.navigate "spaces/#{model.id}/edit"

	App.vent.on "show:space", (model) ->
		API.show null, model
		App.navigate "spaces/#{model.id}"
