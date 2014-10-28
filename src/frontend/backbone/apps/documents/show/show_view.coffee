@Gasoline.module "DocumentsApp.Show", (Show, App, Backbone, Marionette, $, _) ->
    
    class Show.LayoutView extends App.Views.LayoutView
        template: "documents/show/show_layout"
        className: "document-layout"
        regions:
            documentHeaderRegion: "#document-header-region"
            documentRegion: "#document-region"
            tagsRegion: "#tags-region"
            commentsRegion: "#comments-region"

    class Show.Document extends App.Views.ItemView
        template: "documents/show/_document"
        tagName: "div"
