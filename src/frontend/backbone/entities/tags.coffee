@Gasoline.module "Entities", (Entities, App, Backbone, Marionette, $, _) ->

    baseUrl = "/api/v1/documents"

    class Entities.Tag extends Entities.Model
        urlRoot: ->
            "#{baseUrl}/#{@space}/#{@docId}/tags"

        initialize: (attributes, options) ->
            @space = options.space
            @docId = options.docId

    class Entities.TagsCollection extends Entities.Collection
        model: Entities.Tag

    API =
        extractTags: (document, params = {}) ->
            _.defaults params, {}
            
            tags = new Entities.TagsCollection
            tagsArray = []
            document.get("tags").forEach (tag) =>
                tagsArray.push
                    id: tag
                    tag: tag
                    space: document.get("space")
                    docId: document.get("id")
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
