@Gasoline.module "UsersApp.List", (List, App, Backbone, Marionette, $, _) ->
    
    class List.LayoutView extends App.Views.LayoutView
        template: "users/list/list_layout"
        regions:
            panelRegion:        "#panel-region"
            newRegion:          "#new-region"
            usersRegion:        "#users-region"
            paginationRegion:   "#pagination-region"

    class List.User extends App.Views.ItemView
        template: "users/list/_user"
        tagName: "tr"

        modelEvents:
            "updated" : "render"

        triggers:
            "click #edit": "edit:user:clicked"

    class List.Users extends App.Views.CompositeView
        template: "users/list/_users"
        childView: List.User
        childViewContainer: "tbody"
    
    class List.Panel extends App.Views.ItemView
        template: "users/list/_panel"
    
        triggers:
            "click #new-user" : "new:user:button:clicked"

    class List.Pagination extends App.Views.ItemView
        template: "users/list/_pagination"
        className: "pull-right"
