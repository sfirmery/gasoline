@Gasoline.module "DocumentsApp.List", (List, App, Backbone, Marionette, $, _) ->
    
    class List.LayoutView extends App.Views.LayoutView
        template: "documents/list/list_layout"
        regions:
            panelRegion:        "#panel-region"
            documentsRegion:    "#documents-region"
            paginationRegion:   "#pagination-region"

    class List.Document extends App.Views.ItemView
        template: "documents/list/_document"
        tagName: "tr"

    class List.Documents extends App.Views.CompositeView
        template: "documents/list/_documents"
        childView: List.Document
        childViewContainer: "tbody"
    
    class List.Panel extends App.Views.ItemView
        template: "documents/list/_panel"
    
    class List.Pagination extends App.Views.ItemView
        template: "documents/list/_pagination"
        className: "pull-right"
