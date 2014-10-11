@Gasoline.module "DocumentsTagsApp", (DocumentsTagsApp, App, Backbone, Marionette, $, _) ->

    API =
        list: (document, region) ->
            new DocumentsTagsApp.List.Controller
                document: document
                region: region
    
    App.commands.setHandler "show:documents:tags", (document, region) ->
        API.list document, region
