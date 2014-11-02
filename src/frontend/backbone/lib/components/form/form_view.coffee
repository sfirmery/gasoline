@Gasoline.module "Components.Form", (Form, App, Backbone, Marionette, $, _) ->

    class Form.FormLayout extends App.Views.LayoutView
        template: "form/form"

        tagName: "div"
        attributes: ->
          "data-type": @getFormDataType()

        regions:
            headerRegion:   "#form-header-region"
            bodyRegion:     "#form-body-region"
            footerRegion:   "#form-footer-region"

        modelEvents:
            "change:_errors"    : "changeErrors"
            "sync:start"        : "syncStart"
            "sync:stop"         : "syncStop"

        initialize: ->
            { @config } = @options
            if @config.isDialogLayout
                @$el.attr
                    class: "modal-dialog"

            @listenTo @bodyRegion, 'show', =>
                # TODO: fix focus
                @listenTo @bodyRegion.currentView, 'show', =>
                    @focusFirstInput() if @config.focusFirstInput

        serializeData: ->
            footer: @config.footer
            isDialogLayout: @config.isDialogLayout

        focusFirstInput: ->
            console.log "focusFirstInput", @$(":text:enabled:first")
            @$(":text:enabled:first").focus()

        getFormDataType: ->
            if @model.isNew() then "new" else "edit"

        changeErrors: (model, errors, options) ->
            if @config.errors
                if _.isEmpty(errors) then @removeErrors() else @addErrors errors

        removeErrors: ->
            @$(".error").removeClass("error").find("small").remove()

        addErrors: (errors = {}) ->
            for name, array of errors
                @addError name, array[0]

        addError: (name, error) ->
            el = @$("[name='#{name}']:first")
            sm = $("<small>").addClass("error").text(error)
            @insertError(el, sm)

        insertError: (el, sm) ->
            parent = el.closest(".row").addClass("error")
            error_container = parent.find(".error-container")
            if error_container.length then error_container.html(sm) else el.after(sm)

        syncStart: (model) ->
            if @config.syncing
                @addOpacityWrapper true,
                    className: "opacity modal-content"

        syncStop: (model) ->
            @addOpacityWrapper(false) if @config.syncing

        onDestroy: ->
            @addOpacityWrapper(false) if @config.syncing

    class Form.FormHeader extends App.Views.ItemView
        template: "form/header"

        initialize: ->
            { @config } = @options

    class Form.FormFooter extends App.Views.ItemView
        template: "form/footer"

        triggers:
            "submit"                             : "form:submit"
            "click @ui.submit"                   : "form:submit"
            "click [data-form-button='cancel']"  : "form:cancel"

        ui:
            submit: 'button[type="submit"]'

        events:
            "submit":           "submit"
            'click @ui.submit': "submit"

        initialize: ->
            { @config, @buttons } = @options

        serializeData: ->
            footer: @config.footer
            buttons: @buttons?.toJSON() ? false

        submit: (e) ->
            e.preventDefault()
