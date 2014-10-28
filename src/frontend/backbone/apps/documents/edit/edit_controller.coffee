@Gasoline.module "DocumentsApp.Edit", (Edit, App, Backbone, Marionette, $, _) ->

    class Edit.Controller extends App.Controllers.Application

        initialize: (options) ->
            @layout = @getLayoutView()

            # render region when render layout
            @listenTo @layout, "show", =>
                @showHeader document
                @documentView document

            if options.document != null && options.space != null
                document = App.request "documents:entity", options.space, options.document
                
                App.execute "when:fetched", document, =>
                    @show @layout
            else
                document = options.model
                @show @layout

        documentView: (document) ->
            documentView = @getUserView document
            @show documentView, region: @layout.documentRegion
        
        showHeader: (document) ->
            App.execute "show:documents:header", "edit", document, @layout.documentHeaderRegion
        
        getUserView: (document) ->
            new Edit.Document
                model: document
        
        getLayoutView: ->
            new Edit.LayoutView
