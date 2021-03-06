@Gasoline.module "ACLApp", (ACLApp, App, Backbone, Marionette, $, _) ->

    API =
        list: (model) ->
            new ACLApp.List.Controller
                region: App.dialogRegion
                model: model
    
    App.vent.on "list:acl:clicked", (model) ->
        API.list model
