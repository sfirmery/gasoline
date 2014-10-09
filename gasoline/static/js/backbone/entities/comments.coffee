@Gasoline.module "Entities", (Entities, App, Backbone, Marionette, $, _) ->

    baseUrl = "/api/v1/documents"

    class Entities.Comment extends Entities.Model
        urlRoot: ->
            "#{baseUrl}/#{@space}/#{@doc}/comments"

        initialize: (options) ->
            @space = options.space
            @doc = options.doc


    class Entities.CommentsCollection extends Entities.Collection
        model: Entities.Comment

        url: ->
            "#{baseUrl}/#{@space}/#{@doc}/comments"

        initialize: (options) ->
            @space = options.space
            @doc = options.doc

        parse: (resp) ->
            resp

    API =
        # get comment collection for document
        getComments: (space, doc, params = {}) ->
            _.defaults params, {}
            
            comments = new Entities.CommentsCollection
                space: space
                doc: doc
            comments.fetch
                reset: true
                data: params
            comments

        # get a comment of a document
        getComment: (space, document, id, params = {}) ->
            _.defaults params, {}

            comment = new Entities.Comment
                id: id
                space: space
                doc: doc
            comment.fetch
                reset: true
                data: params
            comment

    # request list of comments
    App.reqres.setHandler "comments:entities", (space, document) ->
        API.getComments $.trim(space), $.trim(document)

    # request a comment
    App.reqres.setHandler "comments:entities:one", (space, document, comment) ->
        API.getComment $.trim(space), $.trim(document), $.trim(comment)

    # request an empty comment
    App.reqres.setHandler "comments:entities:empty", (space, document) ->
        new Entities.Comment
            space: $.trim(space)
            doc: $.trim(document)
