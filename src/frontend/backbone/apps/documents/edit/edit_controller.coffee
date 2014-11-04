@Gasoline.module "DocumentsApp.Edit", (Edit, App, Backbone, Marionette, $, _) ->

    class Edit.Controller extends App.Controllers.Application

        initialize: (options) ->
            {model} = options

            documentView = @getDocumentView model

            form = App.request "form:component", documentView,
                buttons:
                    primary: "Submit"
                    cancel: "Cancel"
                onFormCancel: => @trigger "edit:cancel"
                onFormSuccess: => @trigger "edit:success"

            @show form

        getDocumentView: (model) ->
            new Edit.Document
                model: model
