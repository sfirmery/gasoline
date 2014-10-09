@Gasoline.module "TMPLApp.Show", (Show, App, Backbone, Marionette, $, _) ->
    
    class Show.LayoutView extends App.Views.LayoutView
        template: "tmpl/show/templates/show_layout"
        className: "tmpl-layout"
        regions:
            tmplRegion:        "#tmpl-region"

    class Show.TMPL extends App.Views.ItemView
        template: "tmpl/show/templates/_tmpl"
        tagName: "div"
