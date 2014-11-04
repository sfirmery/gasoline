@Gasoline.module "DocumentsApp.Edit", (Edit, App, Backbone, Marionette, $, _) ->

    class Edit.Document extends App.Views.LayoutView
        template: "documents/edit/form"

        dialog: ->
            title: => (if @model.isNew() then "New" else "Edit") + " document"

        serializeData: ->
            isNew: @model.isNew()
