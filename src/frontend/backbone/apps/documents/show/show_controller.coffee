@Gasoline.module "DocumentsApp.Show", (Show, App, Backbone, Marionette, $, _) ->

    class Show.Controller extends App.Controllers.Application

        initialize: (options) ->
            {@mode, @docId, @space} = options
            @layout = @getLayoutView()

            # request document
            document = App.request "documents:entity", @space, @docId

            @on "change:mode", ->
                console.log "change:mode"
                @reload document

            @listenTo document, "edit:document:clicked", =>
                @mode = "edit"
                @trigger "change:mode"

            @listenTo document, "display:document:clicked", =>
                @mode = "show"
                @trigger "change:mode"

            @listenTo @layout, "show", =>
                @headerRegion document
                @documentRegion document
                @tagsRegion document
                @commentsRegion document

            App.execute "when:fetched", document, =>
                @show @layout

        reload: (document) ->
            console.log "reload", document
            @headerRegion document
            @documentRegion document
            @tagsRegion document
            @commentsRegion document

        editDocument: (document) ->
            console.log "edit:document", document

        documentRegion: (document) ->
            if @mode == "edit"
                documentView = App.request "edit:document", document, @layout.documentRegion
            else
                documentView = @getDocumentView document
                @show documentView, region: @layout.documentRegion
            
            @listenTo documentView, "edit:cancel", =>
                @mode = "show"
                @trigger "change:mode"

        headerRegion: (document) ->
            headerView = App.request "documents:header", @mode, document
            @show headerView, region: @layout.documentHeaderRegion

        tagsRegion: (document) ->
            if @mode =="edit"
                @layout.tagsRegion.reset()
            else
                tagsView = App.request "list:document:tags", document
                @show tagsView, region: @layout.tagsRegion

        commentsRegion: (document) ->
            if @mode =="edit"
                @layout.commentsRegion.reset()
            else
                commentsView = App.request "list:comments", document
                @show commentsView, region: @layout.commentsRegion

        getDocumentView: (document) ->
            new Show.Document
                model: document

        getLayoutView: ->
            new Show.LayoutView
