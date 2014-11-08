@Gasoline.module "Entities", (Entities, App, Backbone, Marionette, $, _) ->

    baseUrl = "/api/v1/documents"

    class Entities.Comment extends Entities.Model
        urlRoot: ->
            "#{baseUrl}/#{@space}/#{@docId}/comments"

        initialize: (attributes, options) ->
            {@space, @docId} = options

    class Entities.CommentsCollection extends Entities.Collection
        model: Entities.Comment

        url: ->
            "#{baseUrl}/#{@space}/#{@docId}/comments"

        initialize: (models, options) ->
            {@space, @docId} = options

        parse: (resp) ->
            resp

    API =
        # get comment collection for document
        getComments: (space, docId, params = {}) ->
            _.defaults params, {}
            
            comments = new Entities.CommentsCollection null,
                space: space
                docId: docId
            comments.fetch
                # reset: true
                data: params
            comments

    # request list of comments
    App.reqres.setHandler "comments:entities", (space, docId) ->
        API.getComments $.trim(space), $.trim(docId)

    # request an empty comment
    App.reqres.setHandler "new:comments:entity", (space, docId) ->
        new Entities.Comment null,
            space: $.trim(space)
            docId: $.trim(docId)
