@Gasoline.module "UsersApp.Edit", (Edit, App, Backbone, Marionette, $, _) ->

    class Edit.Controller extends App.Controllers.Base

        initialize: (options) ->
            user = App.request "users:entities:one", options.user

            @layout = @getLayoutView()

            @listenTo @layout, "show", =>
                @userView user

            App.execute "when:fetched", user, =>
                @show @layout

        userView: (user) ->
            userView = @getUserView user
            @show userView, region: @layout.userRegion
        
        getUserView: (user) ->
            new Edit.User
                model: user
        
        getLayoutView: ->
            new Edit.LayoutView
