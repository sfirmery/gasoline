@Gasoline.module "ACLApp.List", (List, App, Backbone, Marionette, $, _) ->

    class List.LayoutView extends App.Views.LayoutView
        template: "acl/list/list_layout"
        regions:
            panelRegion:    "#panel-region"
            aclRegion:      "#acl-region"

        dialog: ->
            title: => "ACL"
            size: "lg"

    class List.ACE extends App.Views.ItemView
        template: "acl/list/_ace"
        tagName: "tr"

    class List.ACL extends App.Views.CompositeView
        template: "acl/list/_acl"
        childView: List.ACE
        childViewContainer: "tbody"

    class List.Panel extends App.Views.ItemView
        template: "acl/list/_panel"
