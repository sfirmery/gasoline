@Gasoline.module "UsersApp.Show", (Show, App, Backbone, Marionette, $, _) ->

    class Show.Controller extends App.Controllers.Base

        initialize: (options) ->
            if options.user != null
                user = App.request "users:entity", options.user
            else
                user = options.model

            @layout = @getLayoutView()

            @listenTo @layout, "show", =>
                @userView user

            App.execute "when:fetched", user, =>
                @show @layout

        userView: (user) ->
            userView = @getUserView user
            @show userView, region: @layout.userRegion
        
        getUserView: (user) ->
            new Show.User
                model: user
        
        getLayoutView: ->
            new Show.LayoutView
