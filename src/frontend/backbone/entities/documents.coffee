@Gasoline.module "Entities", (Entities, App, Backbone, Marionette, $, _) ->

    baseUrl = "/api/v1/documents"

    class Entities.Document extends Entities.Model
        urlRoot: ->
            "#{baseUrl}/#{@space}"

        initialize: (attributes, options) ->
            console.log "init document", attributes, options
            {@space} = options

        toJSON: (model, options) ->
            url = "#{location.protocol}//#{location.host}"
            json = super options
            json.link = location.href
            json.tinylink = "#{url}/#{json.tinylink}" if json.tinylink
            json

        save: (attrs, options) ->
            attrs.author = @get('author').name or @get('author')
            attrs.last_author = @get('last_author').name or @get('last_author')

            super attrs, options

    class Entities.DocumentsCollection extends Entities.Collection
        model: Entities.Document
        url: ->
            "#{baseUrl}/#{@space}"

        initialize: (models, options) ->
            {@space} = options
        
        parse: (resp) ->
            resp

    API =
        getDocuments: (space, params = {}) ->
            _.defaults params, {}
            
            documents = new Entities.DocumentsCollection null,
                space: space
            documents.fetch
                data: params
            documents

        getDocument: (space, doc, params = {}) ->
            _.defaults params, {}

            document = new Entities.Document id: doc,
                space: space
            document.fetch
                data: params
            document

    # request a document
    App.reqres.setHandler "documents:entity", (space, doc) ->
        API.getDocument $.trim(space), $.trim(doc)

    # request list of documents
    App.reqres.setHandler "documents:entities", (space) ->
        API.getDocuments $.trim(space)
