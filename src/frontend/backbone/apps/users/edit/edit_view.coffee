@Gasoline.module "UsersApp.Edit", (Edit, App, Backbone, Marionette, $, _) ->

    class Edit.User extends App.Views.LayoutView
        template: "users/edit/user"

        dialog: ->
            title: => (if @model.isNew() then "New" else "Edit") + " user"

        serializeData: ->
            isNew: @model.isNew()
