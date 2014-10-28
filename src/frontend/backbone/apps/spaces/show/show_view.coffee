@Gasoline.module "SpacesApp.Show", (Show, App, Backbone, Marionette, $, _) ->
    
    class Show.LayoutView extends App.Views.LayoutView
        template: "spaces/show/show_layout"
        className: "space-layout"
        regions:
            spaceHeaderRegion: "#space-header-region"
            spaceRegion: "#space-region"
            tagsRegion: "#tags-region"
            commentsRegion: "#comments-region"

    class Show.Space extends App.Views.ItemView
        template: "spaces/show/_space"
        tagName: "div"
