@Gasoline.module "Entities", (Entities, App, Backbone, Marionette, $, _) ->

    baseUrl = "/api/v1/users"

    class Entities.User extends Entities.Model
        urlRoot: baseUrl

    class Entities.UsersCollection extends Entities.Collection
        model: Entities.User
        url: baseUrl
        
        parse: (resp) ->
            resp

    API =
        getUsers: (params = {}) ->
            _.defaults params, {}
            
            users = new Entities.UsersCollection
            users.fetch
                reset: true
                data: params
            users

        getUser: (name, params = {}) ->
            _.defaults params, {}

            user = new Entities.User id: name
            user.fetch
                reset: true
                data: params
                success: (item) ->
                    console.log "success", item
            user

    # request list of users
    App.reqres.setHandler "users:entities", ->
        API.getUsers()

    # request an user
    App.reqres.setHandler "users:entities:one", (user) ->
        API.getUser $.trim(user)
