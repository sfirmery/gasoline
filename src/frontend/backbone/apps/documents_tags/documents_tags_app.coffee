@Gasoline.module "DocumentsTagsApp", (DocumentsTagsApp, App, Backbone, Marionette, $, _) ->

    API =
        list: (document, region) ->
            new DocumentsTagsApp.List.Controller
                document: document
    
    App.reqres.setHandler "list:document:tags", (document) ->
        throw new Error "Tags List requires a document to be passed in" if not document
        API.list document
