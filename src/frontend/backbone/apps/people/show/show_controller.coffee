@Gasoline.module "PeopleApp.Show", (Show, App, Backbone, Marionette, $, _) ->

    class Show.Controller extends App.Controllers.Application

        initialize: (options) ->
            user = App.request "people:entity", options.user

            App.execute "when:fetched", user, =>
                @layout = @getLayoutView()

                @listenTo @layout, "show", =>
                    @userRegion user

                @show @layout

        userRegion: (user) ->
            userView = @getUserView user
            @show userView, region: @layout.userRegion

        getUserView: (user) ->
            new Show.User
                model: user
        
        getLayoutView: ->
            new Show.LayoutView
