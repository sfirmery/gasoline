@Gasoline.module "DocumentsHeaderApp.Show", (Show, App, Backbone, Marionette, $, _) ->

    class Show.Header extends App.Views.ItemView
        template: "documents_header/show/header"
        tagName: "div"

        ui:
            edit: '#document-edit-link'
            history: '#document-history-link'
            attachments: '#document-attachments-link'
            rights: '#document-rights-link'
            links: '#document-links-link'
            informations: '#document-informations-link'
            display: '#document-display-link'

        events:
            "click @ui.edit" : ->
                App.vent.trigger "edit:document", @model
            "click @ui.history" : ->
                console.log "history clicked"
            "click @ui.attachments" : ->
                console.log "attachments clicked"
            "click @ui.rights" : ->
                console.log "rights clicked"
            "click @ui.links" : ->
                console.log "links clicked"
            "click @ui.informations" : ->
                console.log "informations clicked"
            "click @ui.display" : ->
                App.vent.trigger "show:document", @model

        initialize: (options) ->
            super
            @mode = options.mode

        templateHelpers: ->
            mode: @mode
