@Gasoline.module "SpacesApp.List", (List, App, Backbone, Marionette, $, _) ->
    
    class List.LayoutView extends App.Views.LayoutView
        template: "spaces/list/list_layout"
        regions:
            panelRegion:        "#panel-region"
            spacesRegion:       "#spaces-region"
            paginationRegion:   "#pagination-region"

    class List.Space extends App.Views.ItemView
        template: "spaces/list/_space"
        tagName: "tr"

        modelEvents:
            "updated" : "render"

        ui:
            edit: '#edit'
            delete: '#delete'

        triggers:
            "click @ui.edit": "edit:space:clicked"
            "click @ui.delete" : "delete:space:clicked"

    class List.Spaces extends App.Views.CompositeView
        template: "spaces/list/_spaces"
        childView: List.Space
        childViewContainer: "tbody"
    
    class List.Panel extends App.Views.ItemView
        template: "spaces/list/_panel"

        triggers:
            "click #new-space" : "new:space:button:clicked"

        collectionEvents:
            "add": "render"
            "remove": "render"

    class List.Pagination extends App.Views.ItemView
        template: "spaces/list/_pagination"
        className: "pull-right"

        collectionEvents:
            "add": "render"
            "remove": "render"
