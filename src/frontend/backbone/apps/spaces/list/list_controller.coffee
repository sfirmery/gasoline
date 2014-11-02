@Gasoline.module "SpacesApp.List", (List, App, Backbone, Marionette, $, _) ->

    class List.Controller extends App.Controllers.Application

        initialize: ->
            spaces = App.request "spaces:entities"

            App.execute "when:fetched", spaces, =>
                @layout = @getLayoutView()

                @listenTo @layout, "show", =>
                    @panelRegion spaces
                    @spacesRegion spaces
                    @paginationRegion spaces

                @show @layout

        panelRegion: (spaces) ->
            panelView = @getPanelView spaces

            @listenTo panelView, "new:space:button:clicked", ->
                App.vent.trigger "new:space:clicked", spaces

            @show panelView, region: @layout.panelRegion
        
        spacesRegion: (spaces) ->
            spacesView = @getPeopleView spaces

            @listenTo spacesView, "childview:edit:space:clicked", (iv, args) ->
                App.vent.trigger "edit:space:clicked", args.model

            @listenTo spacesView, "childview:delete:space:clicked", (iv, args) ->
                confirm = App.request "confirm:component",
                    content: "Confirm delete space and ALL his documents?"
                    onConfirmValidate: =>
                        args.model.destroy
                            wait: true

            @show spacesView, region: @layout.spacesRegion

        paginationRegion: (spaces) ->
            paginationView = @getPaginationView spaces
            @show paginationView, region: @layout.paginationRegion

        getPanelView: (spaces) ->
            new List.Panel
                collection: spaces
        
        getPaginationView: (spaces) ->
            new List.Pagination
                collection: spaces
        
        getPeopleView: (spaces) ->
            new List.Spaces
                collection: spaces
        
        getLayoutView: ->
            new List.LayoutView
