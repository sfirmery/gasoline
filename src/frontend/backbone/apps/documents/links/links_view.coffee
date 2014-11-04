@Gasoline.module "DocumentsApp.Links", (Links, App, Backbone, Marionette, $, _) ->

    class Links.View extends App.Views.ItemView
        template: "documents/links/links"

        dialog: ->
            title: => "Links"
