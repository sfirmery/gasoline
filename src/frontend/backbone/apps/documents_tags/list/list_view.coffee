@Gasoline.module "DocumentsTagsApp.List", (List, App, Backbone, Marionette, $, _) ->

    class List.LayoutView extends App.Views.LayoutView
        template: "documents_tags/list/list_layout"
        tagName: "div"
        className: "document-tag-list"
        regions:
            tagsListRegion: "#document-tag-list-region"
            tagsActionsRegion: "#document-tag-list-actions-region"

    class List.Tag extends App.Views.ItemView
        template: "documents_tags/list/_tag"
        tagName: "span"
        className: "label label-info"

        ui:
            delete: '#tag-delete'

        events:
            "click @ui.delete" : ->
                @model.destroy
                    wait: true

    class List.Tags extends App.Views.CompositeView
        template: "documents_tags/list/_tags"
        childView: List.Tag

    class List.NewTag extends App.Views.FormView
        template: "documents_tags/list/_new_tag"
        className: "form-horizontal"

        ui:
            tag: '[name="tag"]'

        initialize: (options) ->
            {@space, @doc, @collection} = options
            super options

        createModel: ->
            @model = App.request "new:tags:entity", @space, @doc

        updateModel: ->
            @model.set
                # id: @ui.tag.val()
                tag: @ui.tag.val()

            # add model to collection after model sync
            @listenToOnce @model, "sync", (model, resp, options) =>
                @collection.add model

        onSuccess: (model) ->
            App.vent.trigger "tag:saved", model
            model.set
                id: model.get("tag")
