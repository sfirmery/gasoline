@Gasoline.module "Entities", (Entities, App, Backbone, Marionette, $, _) ->

    baseUrl = "/api/v1/documents"

    class Entities.Comment extends Entities.Model
        urlRoot: ->
            "#{baseUrl}/#{@space}/#{@doc}/comments"

        initialize: (options) ->
            {@space, @doc} = options


    class Entities.CommentsCollection extends Entities.Collection
        model: Entities.Comment

        url: ->
            "#{baseUrl}/#{@space}/#{@doc}/comments"

        initialize: (options) ->
            {@space, @doc} = options

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
                # reset: true
                data: params
            comments

    # request list of comments
    App.reqres.setHandler "comments:entities", (space, doc) ->
        API.getComments $.trim(space), $.trim(doc)

    # request an empty comment
    App.reqres.setHandler "new:comments:entity", (space, doc) ->
        new Entities.Comment
            space: $.trim(space)
            doc: $.trim(doc)
