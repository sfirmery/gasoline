@Gasoline.module "Entities", (Entities, App, Backbone, Marionette, $, _) ->

    baseUrl = "/api/v1/documents"

    class Entities.Tag extends Entities.Model
        urlRoot: ->
            {@space, @docId} = @collection if @collection
            "#{baseUrl}/#{@space}/#{@docId}/tags"

        initialize: (attributes, options) ->
            {@space, @docId} = options

    class Entities.TagsCollection extends Entities.Collection
        model: Entities.Tag

        initialize: (attributes, options) ->
            {@space, @docId} = options

    API =
        extractTags: (document, params = {}) ->
            _.defaults params, {}
            
            tags = new Entities.TagsCollection null,
                space: document.get("space")
                docId: document.get("id")

            tagsArray = []
            document.get("tags").forEach (tag) =>
                tagsArray.push
                    id: tag
                    tag: tag
            tags.add tagsArray
            tags

    # request an empty comment
    App.reqres.setHandler "new:tags:entity", (space, docId) ->
        new Entities.Tag null,
            space: $.trim(space)
            docId: $.trim(docId)

    # request an tag
    App.reqres.setHandler "extract:tags:entities", (document) ->
        API.extractTags document
