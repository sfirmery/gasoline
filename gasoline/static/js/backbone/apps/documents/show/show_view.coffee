@Gasoline.module "DocumentsApp.Show", (Show, App, Backbone, Marionette, $, _) ->
    
    class Show.LayoutView extends App.Views.LayoutView
        template: "documents/show/templates/show_layout"
        className: "document-layout"
        regions:
            documentHeaderRegion: "#document-header-region"
            documentRegion: "#document-region"
            commentsRegion: "#comments-region"

    class Show.Document extends App.Views.ItemView
        template: "documents/show/templates/_document"
        tagName: "div"
