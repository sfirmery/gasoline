@Gasoline.module "UsersApp.Show", (Show, App, Backbone, Marionette, $, _) ->

    class Show.Controller extends App.Controllers.Application

        initialize: (options) ->
            if options.user != null
                user = App.request "users:entity", options.user
            else
                user = options.model

            App.execute "when:fetched", user, =>
                @layout = @getLayoutView()

                @listenTo @layout, "show", =>
                    @userRegion user

                @show @layout

        userRegion: (user) ->
            userView = @getUserView user
            @layout.userRegion.show userView
        
        getUserView: (user) ->
            new Show.User
                model: user
        
        getLayoutView: ->
            new Show.LayoutView
