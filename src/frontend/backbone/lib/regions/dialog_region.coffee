@Gasoline.module "Regions", (Regions, App, Backbone, Marionette, $, _) ->

  class Regions.Dialog extends Marionette.Region

    # wrap view in dialog layout
    show: (contentView, options) ->
      dialogOptions = @getDefaultOptions _.result(contentView, "dialog")

      @dialogLayout = if dialogOptions.isDialogLayout then contentView else @getDialogLayout dialogOptions

      @listenTo @dialogLayout, "show", =>
        @setupBindings @dialogLayout, dialogOptions
        @openDialog @dialogLayout, dialogOptions

      super @dialogLayout, options

    getDefaultOptions: (dialogOptions = {}) ->
      _.defaults dialogOptions,
        size: "sm"

    setupBindings: (view, dialogOptions) ->

      # listen to bootstrap close event
      @$el.on "hidden.bs.modal", =>
        @empty()

    openDialog: (contentView, dialogOptions) ->
      @$el.addClass("modal fade")
      @$el.find(".modal-dialog").addClass("modal-#{dialogOptions.size}")
      @$el.find(".modal-title").append(@getTitle(dialogOptions))
      @$el.modal()

    bodyRegion: (contentView) ->
      @dialogLayout.bodyRegion.show contentView.bodyRegion

    footerRegion: (footerView) ->
      @dialogLayout.footerRegion.show footerView

    getDialogLayout: (dialogOptions) ->
      new Regions.DialogLayout
        region: @
        options: dialogOptions

    getTitle: (dialogOptions) ->
      _.result dialogOptions, "title"

    onEmpty: ->
      ## make sure to remove any listeners on the $el here
      @$el.off "hidden.bs.modal"

      @stopListening()
      @$el.modal('hide')

  class Regions.DialogLayout extends App.Views.LayoutView
    template: "regions/dialog_layout"

    tagName: "div"
    className: "modal-dialog"

    regions:
      headerRegion:   "#dialog-header-region"
      bodyRegion:     "#dialog-body-region"
      footerRegion:   "#dialog-footer-region"

    initialize: (options) ->
      console.log "initialize dialogLayout", options
      super options

    serializeData: ->
      console.log "serializeData dialogLayout"
