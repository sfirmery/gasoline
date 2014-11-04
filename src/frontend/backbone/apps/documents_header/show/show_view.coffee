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
            "click @ui.edit" : ->           @model.trigger "edit:document:clicked"
            "click @ui.history" : ->        @model.trigger "history:document:clicked"
            "click @ui.attachments" : ->    @model.trigger "attachments:document:clicked"
            "click @ui.rights" : ->         @model.trigger "rights:document:clicked"
            "click @ui.links" : ->          App.vent.trigger "links:document:clicked", @model
            "click @ui.informations" : ->   @model.trigger "informations:document:clicked"
            "click @ui.display" : ->        @model.trigger "display:document:clicked"

        initialize: (options) ->
            super
            @mode = options.mode

        templateHelpers: ->
            mode: @mode
