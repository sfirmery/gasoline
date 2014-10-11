@Gasoline.module "TMPLApp.List", (List, App, Backbone, Marionette, $, _) ->

	class List.Controller extends App.Controllers.Base

		initialize: ->
			tmpl = App.request "tmpl:entities"
			console.log "tmpl ", tmpl

			@layout = @getLayoutView()

			@listenTo @layout, "show", =>
				console.log "showing"
				@resultsView tmpl
				@tmplView tmpl
				@paginationView tmpl

			App.execute "when:fetched", tmpl, =>
				## perform aggregates / sorting / nesting here
				## this is helpful when you want to perform operations but only after
				## all the required dependencies have been fetched and are available
				console.log "fetched", tmpl.models
				tmpl.reset tmpl.sortBy "name"
				@show @layout

		resultsView: (tmpl) ->
			resultsView = @getResultsView tmpl
			@show resultsView, region: @layout.resultsRegion
		
		tmplView: (tmpl) ->
			tmplView = @getTMPLView tmpl
			@show tmplView, region: @layout.tmplRegion
		
		paginationView: (tmpl) ->
			paginationView = @getPaginationView tmpl
			@show paginationView, region: @layout.paginationRegion
		
		getResultsView: (tmpl) ->
			new List.Results
				collection: tmpl
		
		getPaginationView: (tmpl) ->
			new List.Pagination
				collection: tmpl
		
		getTMPLView: (tmpl) ->
			new List.TMPL
				collection: tmpl
		
		getLayoutView: ->
			new List.LayoutView
