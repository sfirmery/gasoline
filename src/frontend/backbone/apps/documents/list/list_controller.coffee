@Gasoline.module "DocumentsApp.List", (List, App, Backbone, Marionette, $, _) ->

    class List.Controller extends App.Controllers.Application

        initialize: (options) ->
            # documents = if options.space then App.request "documents:entities", options.space else null
            documents = App.request "documents:entities", options.space

            @layout = @getLayoutView()

            @listenTo @layout, "show", =>
                @panelRegion documents
                @documentsRegion documents
                @paginationRegion documents

            App.execute "when:fetched", documents, =>
                console.log "fetched", documents.models
                documents.reset documents.sortBy "name"
                @show @layout

        panelRegion: (documents) ->
            panelView = @getPanelView documents
            @show panelView, region: @layout.panelRegion
        
        documentsRegion: (documents) ->
            documentsView = @getDocumentsView documents
            @show documentsView, region: @layout.documentsRegion
        
        paginationRegion: (documents) ->
            paginationView = @getPaginationView documents
            @show paginationView, region: @layout.paginationRegion
        
        getPanelView: (documents) ->
            new List.Panel
                collection: documents
        
        getPaginationView: (documents) ->
            new List.Pagination
                collection: documents
        
        getDocumentsView: (documents) ->
            new List.Documents
                collection: documents
        
        getLayoutView: ->
            new List.LayoutView
