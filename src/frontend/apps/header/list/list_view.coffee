@Gasoline.module "HeaderApp.List", (List, App, Backbone, Marionette, $, _) ->

    class List.LayoutView extends App.Views.LayoutView
        template: "header/list/templates/list_layout"

        regions:
            navRegion: '#nav-region'

    class List.Nav extends App.Views.ItemView
        template: "header/list/templates/_nav"
        tagName: "nav"
        className: "navbar navbar-default"
        attributes:
            role: "navigation"
