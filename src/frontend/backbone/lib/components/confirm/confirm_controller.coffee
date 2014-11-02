@Gasoline.module "Components.Confirm", (Confirm, App, Backbone, Marionette, $, _) ->

    class Confirm.ConfirmController extends App.Controllers.Application

        initialize: (options = {}) ->
            { @content, @title, onConfirmValidate } = options

            @onConfirmValidate = onConfirmValidate if _.isFunction(onConfirmValidate)

            @confirmView = @getConfirmView()
            @confirmView['dialog'] = {}
            @confirmView['dialog'].isDialogLayout = true

            @setMainView @confirmView

            @listenTo @confirmView, "show", => 
                @listenTo @confirmView, "confirm:valid", => @confirmValid()
                @listenTo @confirmView, "confirm:cancel", => @confirmCancel()

            @show @confirmView

        confirmValid: ->
            @onConfirmValidate()
            App.dialogRegion.empty()

        confirmCancel: ->
            App.dialogRegion.empty()

        getConfirmView: ->
            new Confirm.ConfirmView
                content: @content
                title: @title
                buttons: @getButtons()

        getButtons: ->
            App.request("confirm:button:entities")

    App.reqres.setHandler "confirm:component", (options = {}) ->
        throw new Error "Confirm Component requires a content to be passed in" if not 'content' in options

        options.region = App.dialogRegion
        new Confirm.ConfirmController options
