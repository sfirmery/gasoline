@Gasoline.module "PeopleApp.List", (List, App, Backbone, Marionette, $, _) ->
    
    class List.LayoutView extends App.Views.LayoutView
        template: "people/list/list_layout"
        regions:
            panelRegion:        "#panel-region"
            peopleRegion:       "#people-region"
            paginationRegion:   "#pagination-region"

    class List.User extends App.Views.ItemView
        template: "people/list/_user"
        tagName: "tr"

        modelEvents:
            "updated" : "render"

        ui:
            edit: '#edit'
            delete: '#delete'

        triggers:
            "click @ui.edit": "edit:user:clicked"
            "click @ui.delete" : "delete:user:clicked"

    class List.People extends App.Views.CompositeView
        template: "people/list/_people"
        childView: List.User
        childViewContainer: "tbody"
    
    class List.Panel extends App.Views.ItemView
        template: "people/list/_panel"
    
        triggers:
            "click #new-user" : "new:user:button:clicked"

        collectionEvents:
            "add": "render"
            "remove": "render"

    class List.Pagination extends App.Views.ItemView
        template: "people/list/_pagination"
        className: "pull-right"

        collectionEvents:
            "add": "render"
            "remove": "render"
