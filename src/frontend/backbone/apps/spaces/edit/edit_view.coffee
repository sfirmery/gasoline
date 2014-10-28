@Gasoline.module "SpacesApp.Edit", (Edit, App, Backbone, Marionette, $, _) ->
    
    class Edit.LayoutView extends App.Views.LayoutView
        template: "spaces/edit/edit_layout"
        className: "space-layout"
        regions:
            spaceHeaderRegion: "#space-header-region"
            spaceRegion: "#space-region"

    class Edit.Space extends App.Views.FormView
        template: "spaces/edit/_space"
        className: "space-edit-form form-horizontal"

        ui:
            cancel: '#space-edit-form-cancel'
            description: '[name="description"]'
            activityIndicator: '.loading'

        events:
            "click @ui.cancel" : ->
                App.vent.trigger "show:space", @model
                console.log "cancel clicked", @model

        createModel: ->
            @model

        updateModel: ->
            @model.set
                description: @ui.description.val()

        onSuccess: (model) ->
            console.log "success save", model
            App.vent.trigger "space:saved", model
