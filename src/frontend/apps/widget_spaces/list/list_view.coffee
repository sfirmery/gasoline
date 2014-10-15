@Gasoline.module "WidgetSpacesApp.List", (List, App, Backbone, Marionette, $, _) ->
    
    class List.Space extends App.Views.ItemView
        template: "widget_spaces/list/templates/_space"
        tagName: "li"

    class List.Spaces extends App.Views.CollectionView
        childView: List.Space
