@Gasoline.module "DocumentsApp.Edit", (Edit, App, Backbone, Marionette, $, _) ->

    class Edit.Controller extends App.Controllers.Application

        initialize: (options) ->
            {model} = options
            # @layout = @getLayoutView()
            # @setMainView @layout

            documentView = @getDocumentView model

            form = App.request "form:component", documentView,
                buttons:
                    primary: "Submit"
                    cancel: "Cancel"
                # onFormCancel: => @region.empty()
                # onFormSuccess: => @region.empty()

            # @listenTo @layout, "show", =>
            @listenTo form, "form:cancel", =>
                console.log "trap form:cancel"
                @trigger "edit:cancel"

            console.log "show edit layout", @layout
            @show form

        show: (options) ->
            console.log "show edit Controller wiht options", options
            super options

        getDocumentView: (model) ->
            new Edit.Document
                model: model

        getLayoutView: ->
            new Edit.LayoutView
