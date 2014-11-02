@Gasoline.module "DocumentsTagsApp.List", (List, App, Backbone, Marionette, $, _) ->

    class List.Controller extends App.Controllers.Application

        initialize: (options) ->
            @space = options.document.get('space')
            @doc = options.document.id

            @layout = @getLayoutView()

            @listenTo @layout, "show", =>
                # extract tags from document
                tags = App.request "extract:tags:entities", options.document

                # fill regions
                @tagsListRegion tags
                @tagsActionsRegion tags

            # define main view
            @setMainView @layout

        tagsListRegion: (tags) ->
            tagsView = @getTagsView tags
            @show tagsView, region: @layout.tagsListRegion

        tagsActionsRegion: (tags) ->
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
