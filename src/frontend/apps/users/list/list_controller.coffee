@Gasoline.module "UsersApp.List", (List, App, Backbone, Marionette, $, _) ->

	class List.Controller extends App.Controllers.Base

		initialize: ->
			users = App.request "users:entities"

			@layout = @getLayoutView()

			@listenTo @layout, "show", =>
				@resultsView users
				@usersView users
				@paginationView users

			App.execute "when:fetched", users, =>
				users.reset users.sortBy "name"
				@show @layout

		resultsView: (users) ->
			resultsView = @getResultsView users
			@show resultsView, region: @layout.resultsRegion
		
		usersView: (users) ->
			usersView = @getUsersView users
			@show usersView, region: @layout.usersRegion
		
		paginationView: (users) ->
			paginationView = @getPaginationView users
			@show paginationView, region: @layout.paginationRegion
		
		getResultsView: (users) ->
			new List.Results
				collection: users
		
		getPaginationView: (users) ->
			new List.Pagination
				collection: users
		
		getUsersView: (users) ->
			new List.Users
				collection: users
		
		getLayoutView: ->
			new List.LayoutView
