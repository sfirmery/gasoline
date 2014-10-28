@Gasoline.module "UsersApp.List", (List, App, Backbone, Marionette, $, _) ->

  class List.Controller extends App.Controllers.Application

    initialize: ->
      users = App.request "users:entities"

      App.execute "when:fetched", users, =>

        @layout = @getLayoutView()

        @listenTo @layout, "show", =>
          @panelRegion users
          @usersRegion users
          @paginationRegion users

        @show @layout

    panelRegion: (users) ->
      panelView = @getPanelView users

      @listenTo panelView, "new:user:button:clicked", ->
        App.vent.trigger "new:user:clicked", users

      @show panelView, region: @layout.panelRegion
    
    usersRegion: (users) ->
      usersView = @getUsersView users

      @listenTo usersView, "childview:edit:user:clicked", (iv, args) ->
        App.vent.trigger "edit:user:clicked", args.model

      @show usersView, region: @layout.usersRegion

    paginationRegion: (users) ->
      paginationView = @getPaginationView users
      @show paginationView, region: @layout.paginationRegion

    getPanelView: (users) ->
      new List.Panel
        collection: users
    
    getPaginationView: (users) ->
      new List.Pagination
        collection: users
    
    getUsersView: (users) ->
      new List.Users
        collection: users
    
    getLayoutView: ->
      new List.LayoutView
