@Gasoline.module "Entities", (Entities, App, Backbone, Marionette, $, _) ->

    baseUrl = "/api/v1/documents"

    class Entities.Tag extends Entities.Model
        urlRoot: ->
            "#{baseUrl}/#{@space}/#{@doc}/tags"

        initialize: (options) ->
            @space = options.space or @model.get("space")
            @doc = options.doc or @model.get("doc")

    class Entities.TagsCollection extends Entities.Collection
        model: Entities.Tag

    API =
        getTags: (params = {}) ->
            _.defaults params, {}
            
            tags = new Entities.TagsCollection
            tags.fetch
                reset: true
                data: params
            tags

        extractTags: (document, params = {}) ->
            _.defaults params, {}
            
            console.log "extractTags from document", document
            tags = new Entities.TagsCollection
            tagsArray = []
            document.get("tags").forEach (tag) =>
                tagsArray.push
                    id: tag
                    tag: tag
                    space: document.get("space")
                    doc: document.get("id")
            tags.add tagsArray
            console.log "extractTags", tags, tagsArray
            tags

        getTag: (name, params = {}) ->
            _.defaults params, {}

            tag = new Entities.Tag id: name
            tag.fetch
                reset: true
                data: params
                success: (item) ->
                    console.log "success", item
            tag

    # request an empty comment
    App.reqres.setHandler "tags:entities:empty", (space, document) ->
        new Entities.Tag
            space: $.trim(space)
            doc: $.trim(document)

    # request an tag
    App.reqres.setHandler "tags:entities:extract", (document) ->
        API.extractTags document
