@Gasoline.module "UsersApp.Edit", (Edit, App, Backbone, Marionette, $, _) ->
    
    class Edit.LayoutView extends App.Views.LayoutView
        template: "users/edit/templates/edit_layout"
        className: "user-layout"
        regions:
            userRegion:        "#user-region"

    class Edit.User extends App.Views.FormView
        template: "users/edit/templates/_user"
        className: "user-edit-form"

        ui:
            description: '[name="description"]'
            activityIndicator: '.loading'

        createModel: ->
            @model

        updateModel: ->
            @model.set
                description: @ui.description.val()

        onSuccess: (model) ->
            console.log "success save", model
            # Backbone.trigger 'user:saved', model
            # model.trigger 'user:saved', model
            App.vent.trigger "user:saved", model
