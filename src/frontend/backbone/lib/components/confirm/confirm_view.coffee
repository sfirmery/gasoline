@Gasoline.module "Components.Confirm", (Confirm, App, Backbone, Marionette, $, _) ->

    class Confirm.ConfirmView extends App.Views.ItemView
        template: "confirm/confirm"

        tagName: "div"
        className: "modal-dialog"

        ui:
            cancel: '[data-form-button="cancel"]'
            valid: '[data-form-button="primary"]'

        triggers:
            "click @ui.cancel" : "confirm:cancel"
            "click @ui.valid" :  "confirm:valid"

        initialize: ->
            { @buttons, @title, @content } = @options

        serializeData: ->
            buttons: @buttons?.toJSON() ? false
            content: @content
            title: @title
