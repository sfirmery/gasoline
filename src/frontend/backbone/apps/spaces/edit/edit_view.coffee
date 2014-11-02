@Gasoline.module "SpacesApp.Edit", (Edit, App, Backbone, Marionette, $, _) ->
    
    class Edit.Space extends App.Views.LayoutView
        template: "spaces/edit/space"

        dialog: ->
            title: => (if @model.isNew() then "New" else "Edit") + " space"

        serializeData: ->
            isNew: @model.isNew()
