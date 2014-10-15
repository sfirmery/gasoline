@Gasoline.module "Entities", (Entities, App, Backbone, Marionette, $, _) ->

    baseUrl = "/api/v1/documents"

    class Entities.Document extends Entities.Model
        urlRoot: ->
            "#{baseUrl}/#{@space}"

        initialize: (options) ->
            {@space} = options

    class Entities.DocumentsCollection extends Entities.Collection
        model: Entities.Document
        url: ->
            "#{baseUrl}/#{@space}"

        initialize: (options) ->
            {@space} = options
        
        parse: (resp) ->
            resp

    API =
        getDocuments: (space, params = {}) ->
            _.defaults params, {}
            
            documents = new Entities.DocumentsCollection
                space: space
            documents.fetch
                data: params
            documents

        getDocument: (space, doc, params = {}) ->
            _.defaults params, {}

            document = new Entities.Document
                space: space
                id: doc
            document.fetch
                data: params
            document

    # request a document
    App.reqres.setHandler "documents:entity", (space, doc) ->
        API.getDocument $.trim(space), $.trim(doc)

    # request list of documents
    App.reqres.setHandler "documents:entities", (space) ->
        API.getDocuments $.trim(space)
