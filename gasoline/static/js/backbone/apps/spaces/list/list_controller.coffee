@Gasoline.module "SpacesApp.List", (List, App, Backbone, Marionette, $, _) ->

	class List.Controller extends App.Controllers.Base

		initialize: (options) ->
			console.log options
			if options.space != null
				spaces = App.request "spaces:entities", options.space
				console.log "spaces ", spaces
			else
				spaces = null

			@layout = @getLayoutView()

			@listenTo @layout, "show", =>
				console.log "showing"
				@resultsView spaces
				@spacesView spaces
				@paginationView spaces

			App.execute "when:fetched", spaces, =>
				console.log "fetched", spaces.models
				spaces.reset spaces.sortBy "name"
				@show @layout

		resultsView: (spaces) ->
			resultsView = @getResultsView spaces
			@show resultsView, region: @layout.resultsRegion
		
		spacesView: (spaces) ->
			spacesView = @getSpacesView spaces
			@show spacesView, region: @layout.spacesRegion
		
		paginationView: (spaces) ->
			paginationView = @getPaginationView spaces
			@show paginationView, region: @layout.paginationRegion
		
		getResultsView: (spaces) ->
			new List.Results
				collection: spaces
		
		getPaginationView: (spaces) ->
			new List.Pagination
				collection: spaces
		
		getSpacesView: (spaces) ->
			new List.Spaces
				collection: spaces
		
		getLayoutView: ->
			new List.LayoutView
