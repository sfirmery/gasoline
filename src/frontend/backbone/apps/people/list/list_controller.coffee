@Gasoline.module "PeopleApp.List", (List, App, Backbone, Marionette, $, _) ->

    class List.Controller extends App.Controllers.Application

        initialize: ->
            people = App.request "people:entities"

            App.execute "when:fetched", people, =>
                @layout = @getLayoutView()

                @listenTo @layout, "show", =>
                    @panelRegion people
                    @peopleRegion people
                    @paginationRegion people

                @show @layout

        panelRegion: (people) ->
            panelView = @getPanelView people

            @listenTo panelView, "new:user:button:clicked", ->
                App.vent.trigger "new:user:clicked", people

            @show panelView, region: @layout.panelRegion
        
        peopleRegion: (people) ->
            peopleView = @getPeopleView people

            @listenTo peopleView, "childview:edit:user:clicked", (iv, args) ->
                App.vent.trigger "edit:user:clicked", args.model

            @listenTo peopleView, "childview:delete:user:clicked", (iv, args) ->
                confirm = App.request "confirm:component",
                    content: "Confirm delete user?"
                    onConfirmValidate: =>
                        args.model.destroy
                            wait: true

            @show peopleView, region: @layout.peopleRegion

        paginationRegion: (people) ->
            paginationView = @getPaginationView people
            @show paginationView, region: @layout.paginationRegion

        getPanelView: (people) ->
            new List.Panel
                collection: people
        
        getPaginationView: (people) ->
            new List.Pagination
                collection: people
        
        getPeopleView: (people) ->
            new List.People
                collection: people
        
        getLayoutView: ->
            new List.LayoutView
