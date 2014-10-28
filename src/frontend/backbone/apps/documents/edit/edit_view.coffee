@Gasoline.module "DocumentsApp.Edit", (Edit, App, Backbone, Marionette, $, _) ->
    
    class Edit.LayoutView extends App.Views.LayoutView
        template: "documents/edit/edit_layout"
        className: "document-layout"
        regions:
            documentHeaderRegion: "#document-header-region"
            documentRegion: "#document-region"

    class Edit.Document extends App.Views.FormView
        template: "documents/edit/_document"
        className: "document-edit-form form-horizontal"

        ui:
            title: '[name="title"]'
            content: '[name="content"]'
            cancel: '#document-edit-form-cancel'
            activityIndicator: '.loading'

        events:
            "click @ui.cancel" : ->
                App.vent.trigger "show:document", @model
                console.log "cancel clicked", @model

        createModel: ->
            @model

        updateModel: ->
            @model.set
                title: @ui.title.val()
                content: @ui.content.val()
                author: @model.get('author').name or @model.get('author')
                last_author: @model.get('last_author').name or @model.get('last_author')

        onSuccess: (model) ->
            console.log "success save", model
            # Backbone.trigger 'document:saved', model
            # model.trigger 'document:saved', model
            App.vent.trigger "document:saved", model
