@Gasoline.module "PeopleApp.Show", (Show, App, Backbone, Marionette, $, _) ->
    
    class Show.LayoutView extends App.Views.LayoutView
        template: "people/show/show_layout"
        className: "user-layout"
        regions:
            userRegion: "#user-region"

    class Show.User extends App.Views.ItemView
        template: "people/show/_user"
        tagName: "div"
        className: "user-profile"

        modelEvents:
            "updated" : "render"

        ui:
            edit: '#edit'

        events:
            "click @ui.edit": ->
                App.vent.trigger "edit:user:clicked", @model
