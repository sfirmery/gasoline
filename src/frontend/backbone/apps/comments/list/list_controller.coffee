@Gasoline.module "CommentsApp.List", (List, App, Backbone, Marionette, $, _) ->

    class List.Controller extends App.Controllers.Application

        initialize: (options) ->
            if options.model != null
                @space = options.model.get('space')
                @doc = options.model.id
                comments = App.request "comments:entities", @space, @doc
            else
                comments = null

            @layout = @getLayoutView()

            @listenTo @layout, "show", =>
                @commentsView comments
                @newCommentView comments

            App.execute "when:fetched", comments, =>
                comments.reset comments.sortBy "date"
                @show @layout

        commentsView: (comments) ->
            commentsView = @getCommentsView comments
            @show commentsView, region: @layout.commentsRegion

        newCommentView: (comments) ->
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
