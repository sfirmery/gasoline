@Gasoline.module "Entities", (Entities, App, Backbone, Marionette, $, _) ->

    baseUrl = "/api/v1/documents"

    class Entities.Document extends Entities.Model
        urlRoot: baseUrl

    class Entities.DocumentsCollection extends Entities.Collection
        model: Entities.Document
        url: baseUrl
        
        parse: (resp) ->
            resp

    API =
        getDocuments: (space, params = {}) ->
            _.defaults params, {}
            
            documents = new Entities.DocumentsCollection
            documents.url = "#{documents.url}/#{space}"
            documents.fetch
                reset: true
                data: params
                # success: (item) ->
                #     console.log "success", item.models
            documents

        getDocument: (space, id, params = {}) ->
            _.defaults params, {}

            document = new Entities.Document id: id
            document.urlRoot = "#{document.urlRoot}/#{space}"
            document.fetch
                reset: true
                data: params
                # success: (item) ->
                #     console.log "success", item
            document

    # request list of documents
    App.reqres.setHandler "documents:entities", (space) ->
        API.getDocuments $.trim(space)

    # request a document
    App.reqres.setHandler "documents:entities:one", (space, document) ->
        API.getDocument $.trim(space), $.trim(document)
