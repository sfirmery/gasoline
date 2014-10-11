@Gasoline.module "TMPLApp", (TMPLApp, App, Backbone, Marionette, $, _) ->

	class TMPLApp.Router extends Marionette.AppRouter
		appRoutes:
			"tmpl": "list"
			"tmpl/:tmpl": "show"
		
	API =
		list: ->
			new TMPLApp.List.Controller
		show: (tmpl) ->
			new TMPLApp.Show.Controller tmpl
			
	App.addInitializer ->
		new TMPLApp.Router
			controller: API
	