@Gasoline.module "Entities", (Entities, App, Backbone, Marionette, $, _) ->

    class Entities.Button extends Entities.Model
        defaults:
            buttonType: "button"

    class Entities.ButtonsCollection extends Entities.Collection
        model: Entities.Button

    API =
        getFormButtons: (buttons, model) ->
            buttons = @getDefaultButtons buttons, model

            array = []
            array.push { type: "cancel",  className: "btn btn-default", text: buttons.cancel                        } unless buttons.cancel is false
            array.push { type: "primary", className: "btn btn-primary", text: buttons.primary, buttonType: "submit" } unless buttons.primary is false

            array.reverse() if buttons.placement is "left"

            buttonCollection = new Entities.ButtonsCollection array
            buttonCollection.placement = buttons.placement
            buttonCollection

        getConfirmButtons: ->
            array = []
            array.push { type: "cancel",  className: "btn btn-default", text: "Cancel"  }
            array.push { type: "primary", className: "btn btn-primary", text: "OK" }

            buttonCollection = new Entities.ButtonsCollection array
            buttonCollection.placement = "left"
            buttonCollection

        getDefaultButtons: (buttons, model) ->
            _.defaults buttons,
                primary: if model.isNew() then "Create" else "Save Changes"
                cancel: "Cancel"
                placement: "right"

    App.reqres.setHandler "form:button:entities", (buttons = {}, model) ->
        API.getFormButtons buttons, model

    App.reqres.setHandler "confirm:button:entities", ->
        API.getConfirmButtons()
