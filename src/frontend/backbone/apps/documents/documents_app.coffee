@Gasoline.module "DocumentsApp", (DocumentsApp, App, Backbone, Marionette, $, _) ->

    class DocumentsApp.Router extends Marionette.AppRouter
        appRoutes:
            "documents/:space": "list"
            "documents/:space/:docId": "show"
            "documents/:space/:docId/:mode": "show"
        
    API =
        list: (space) ->
            new DocumentsApp.List.Controller
                space: space

        show: (space, docId, mode = "show") ->
            new DocumentsApp.Show.Controller
                mode: mode
                space: space
                docId: docId

        edit: (model, region) ->
            new DocumentsApp.Edit.Controller
                model: model
                region: region

    App.reqres.setHandler "edit:document", (model, region) ->
        throw new Error "Comments List requires a model to be passed in" if not model
        console.log "request edit:document"
        API.edit model, region

    App.addInitializer ->
        new DocumentsApp.Router
            controller: API
