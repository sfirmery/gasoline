@Gasoline.module "DocumentsApp", (DocumentsApp, App, Backbone, Marionette, $, _) ->

	class DocumentsApp.Router extends Marionette.AppRouter
		appRoutes:
			"documents/:space": "list"
			"documents/:space/:document": "show"
			"documents/:space/:document/edit": "edit"
		
	API =
		list: (space) ->
			new DocumentsApp.List.Controller
				space: space

		show: (space, document, model) ->
			new DocumentsApp.Show.Controller
				space: space
				document: document
				model: model

		edit: (space, document, model) ->
			new DocumentsApp.Edit.Controller
				space: space
				document: document
				model: model

	App.addInitializer ->
		new DocumentsApp.Router
			controller: API

	App.vent.on "document:saved", (model) ->
        App.vent.trigger "show:document", model

	App.vent.on "edit:document", (model) ->
		API.edit null, null, model
		App.navigate "documents/#{model.get('space')}/#{model.id}/edit"

	App.vent.on "show:document", (model) ->
		API.show null, null, model
		App.navigate "documents/#{model.get('space')}/#{model.id}"
