@Gasoline.module "SpacesApp.Edit", (Edit, App, Backbone, Marionette, $, _) ->

    class Edit.Controller extends App.Controllers.Application

        initialize: (options) ->
            { spaces, space } = options
            space ?= App.request "new:space:entity"

            spaceView = @getSpaceView spaces, space

            form = App.request "form:component", spaceView,
                proxy: "dialog"
                proxyLayout: true
                onFormCancel: => @region.empty()
                onFormSuccess: => @region.empty()

            @show form

        getSpaceView: (spaces, space) ->
            new Edit.Space
                collection: spaces
                model: space
