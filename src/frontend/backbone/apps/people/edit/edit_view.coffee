@Gasoline.module "PeopleApp.Edit", (Edit, App, Backbone, Marionette, $, _) ->

    class Edit.User extends App.Views.LayoutView
        template: "people/edit/user"

        dialog: ->
            title: => (if @model.isNew() then "New" else "Edit") + " user"
            size: "lg"

        serializeData: ->
            isNew: @model.isNew()
