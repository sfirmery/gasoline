@Gasoline.module "DashboardApp.Show", (Show, App, Backbone, Marionette, $, _) ->

	class Show.Controller extends App.Controllers.Base

		initialize: ->
			@layout = @getLayoutView()

			@listenTo @layout, "show", =>
				@listUsers()

			@show @layout
		
		listUsers: ->
			App.execute "users:entities", @layout.usersRegion
			console.log "list users end"

		getLayoutView: ->
			new Show.LayoutView