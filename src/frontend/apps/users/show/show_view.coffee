@Gasoline.module "UsersApp.Show", (Show, App, Backbone, Marionette, $, _) ->
    
    class Show.LayoutView extends App.Views.LayoutView
        template: "users/show/templates/show_layout"
        className: "user-layout"
        regions:
            userRegion:        "#user-region"

    class Show.User extends App.Views.ItemView
        template: "users/show/templates/_user"
        tagName: "div"
        className: "user-profile"
