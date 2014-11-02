@Gasoline.module "Components.Form", (Form, App, Backbone, Marionette, $, _) ->

    class Form.FormController extends App.Controllers.Application

        defaults: ->
            footer: true
            focusFirstInput: true
            errors: true
            syncing: true
            proxy: false
            proxyLayout: false
            onFormSubmit: ->
            onFormCancel: ->
            onFormSuccess: ->

        initialize: (options = {}) ->
            { @contentView } = options

            @model      = @getModel options
            @collection = @getCollection options

            config = @getConfig options

            @formLayout = @getFormLayout config
            @setMainView @formLayout

            @parseProxys config.proxy, config if config.proxy
            @createListeners config

        createListeners: (config) ->
            @listenTo @formLayout, "show", => 
                @bodyRegion()

                if config.footer
                    @footerRegion config
                    @listenTo @footerView, "form:submit", => @formSubmit(config)
                    @listenTo @footerView, "form:cancel", => @formCancel(config)

        getConfig: (options) ->
            form = _.result @contentView, "form"

            config = @mergeDefaultsInto(form)

            _.extend config, _(options).omit("contentView", "model", "collection")
            _.extend config,
                isDialogLayout: 'dialog' in _([config.proxy]).flatten()

        getModel: (options) ->
            ## pull model off of contentView by default
            ## allow options.model to override
            ## or instantiate a new model if nothing is present
            model = options.model or @contentView.model
            if options.model is false
                model = App.request "new:model"
                @_saveModel = false
            model

        getCollection: (options) ->
            options.collection or @contentView.collection

        parseProxys: (proxys, config) ->
            for proxy in _([proxys]).flatten()
                @formLayout[proxy] = _.result @contentView, proxy
                @formLayout[proxy].isDialogLayout = config.isDialogLayout

        formCancel: (config) ->
            config.onFormCancel()
            @trigger "form:cancel"

        formSubmit: (config) ->
            ## pull data off of form
            data = Backbone.Syphon.serialize @formLayout

            ## notify our controller instance in case things are listening to it
            @trigger("form:submit", data)

            @processModelSave(data, config) unless @_shouldNotProcessModelSave(config, data)

        _shouldNotProcessModelSave: (config, data) ->
            @_saveModel is false or config.onFormSubmit is false or config.onFormSubmit?(data) is false

        processModelSave: (data, config) ->
            console.log "processModelSave", @model, @collection, data, config
            @model.save data,
                collection: @collection
                callback: config.onFormSuccess

            console.log "processModelSaved", @model, @collection

        bodyRegion: ->
            @show @contentView, region: @formLayout.bodyRegion
            Backbone.Syphon.deserialize @formLayout, @model.toJSON()

        footerRegion: (config) ->
            @footerView = @getFooterView config
            @show @footerView, region: @formLayout.footerRegion

        getFooterView: (config) ->
            new Form.FormFooter
                config: config
                model: @model
                buttons: @getButtons config.buttons

        getFormLayout: (config) ->
            new Form.FormLayout
                config: config
                model: @model

        getButtons: (buttons = {}) ->
            App.request("form:button:entities", buttons, @contentView.model) unless buttons is false

    App.reqres.setHandler "form:component", (contentView, options = {}) ->
        throw new Error "Form Component requires a contentView to be passed in" if not contentView

        options.contentView = contentView
        new Form.FormController options
