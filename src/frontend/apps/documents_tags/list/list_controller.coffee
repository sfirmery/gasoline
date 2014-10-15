@Gasoline.module "DocumentsTagsApp.List", (List, App, Backbone, Marionette, $, _) ->

    class List.Controller extends App.Controllers.Base

        initialize: (options) ->
            tags = App.request "extract:tags:entities", options.document
            @space = options.document.get('space')
            @doc = options.document.id

            @layout = @getLayoutView()

            @listenTo @layout, "show", =>
                @tagsView tags
                @newTagView tags

            @show @layout

        tagsView: (tags) ->
            tagsView = @getTagsView tags
            @show tagsView, region: @layout.tagsRegion

        newTagView: (tags) ->
            newTagView = @getNewTagView tags
            @show newTagView, region: @layout.tagsActionsRegion

        getTagsView: (tags) ->
            new List.Tags
                collection: tags

        getNewTagView: (tags) ->
            new List.NewTag
                collection: tags
                space: @space
                doc: @doc

        getLayoutView: ->
            new List.LayoutView
