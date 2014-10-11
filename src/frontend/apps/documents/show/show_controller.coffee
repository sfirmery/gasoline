@Gasoline.module "DocumentsApp.Show", (Show, App, Backbone, Marionette, $, _) ->

    class Show.Controller extends App.Controllers.Base

        initialize: (options) ->
            @layout = @getLayoutView()

            # render region when render layout
            @listenTo @layout, "show", =>
                @showHeader document
                @documentView document
                @showTags document
                @showComments document

            if options.document != null && options.space != null
                document = App.request "documents:entities:one", options.space, options.document

                App.execute "when:fetched", document, =>
                    @show @layout
            else
                document = options.model
                @show @layout

        documentView: (document) ->
            documentView = @getDocumentView document
            @show documentView, region: @layout.documentRegion

        showHeader: (document) ->
            App.execute "show:documents:header", "show", document, @layout.documentHeaderRegion
        
        showTags: (document) ->
            App.execute "show:documents:tags", document, @layout.tagsRegion

        showComments: (document) ->
            App.execute "show:comments", document, @layout.commentsRegion

        getDocumentView: (document) ->
            new Show.Document
                model: document

        getLayoutView: ->
            new Show.LayoutView
