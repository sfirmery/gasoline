@Gasoline.module "CommentsApp.List", (List, App, Backbone, Marionette, $, _) ->

    class List.Controller extends App.Controllers.Application

        initialize: (options) ->
            if options.model != null
                @space = options.model.get('space')
                @doc = options.model.id

            @layout = @getLayoutView()

            @listenTo @layout, "show", =>
                # request document comments
                comments = if options.model then App.request "comments:entities", @space, @doc else null

                App.execute "when:fetched", comments, =>
                    # fill regions
                    @commentsRegion comments
                    @commentsActionsRegion comments

            # define main view
            @setMainView @layout

        commentsRegion: (comments) ->
            commentsView = @getCommentsView comments
            @show commentsView, region: @layout.commentsRegion

        commentsActionsRegion: (comments) ->
            newCommentView = @getNewCommentView comments
            @show newCommentView, region: @layout.commentsActionsRegion
        
        getCommentsView: (comments) ->
            new List.Comments
                collection: comments

        getNewCommentView: (comments) ->
            new List.NewComment
                collection: comments
                space: @space
                doc: @doc
        
        getLayoutView: ->
            new List.LayoutView
