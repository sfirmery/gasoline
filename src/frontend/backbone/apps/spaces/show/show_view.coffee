@Gasoline.module "SpacesApp.Show", (Show, App, Backbone, Marionette, $, _) ->
    
    class Show.LayoutView extends App.Views.LayoutView
        template: "spaces/show/show_layout"
        className: "space-layout"
        regions:
            spaceRegion: "#space-region"

    class Show.Space extends App.Views.ItemView
        template: "spaces/show/_space"
        tagName: "div"

        modelEvents:
            "updated" : "render"

        ui:
            edit: '#edit'

        events:
            "click @ui.edit": ->
                App.vent.trigger "edit:space:clicked", @model
