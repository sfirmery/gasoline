@Gasoline.module "DocumentsApp.List", (List, App, Backbone, Marionette, $, _) ->

	class List.Controller extends App.Controllers.Base

		initialize: (options) ->
			console.log options
			if options.space != null
				documents = App.request "documents:entities", options.space
				console.log "documents ", documents
			else
				documents = null

			@layout = @getLayoutView()

			@listenTo @layout, "show", =>
				console.log "showing"
				@resultsView documents
				@documentsView documents
				@paginationView documents

			App.execute "when:fetched", documents, =>
				## perform aggregates / sorting / nesting here
				## this is helpful when you want to perform operations but only after
				## all the required dependencies have been fetched and are available
				console.log "fetched", documents.models
				documents.reset documents.sortBy "name"
				@show @layout

		resultsView: (documents) ->
			resultsView = @getResultsView documents
			@show resultsView, region: @layout.resultsRegion
		
		documentsView: (documents) ->
			documentsView = @getDocumentsView documents
			@show documentsView, region: @layout.documentsRegion
		
		paginationView: (documents) ->
			paginationView = @getPaginationView documents
			@show paginationView, region: @layout.paginationRegion
		
		getResultsView: (documents) ->
			new List.Results
				collection: documents
		
		getPaginationView: (documents) ->
			new List.Pagination
				collection: documents
		
		getDocumentsView: (documents) ->
			new List.Documents
				collection: documents
		
		getLayoutView: ->
			new List.LayoutView
