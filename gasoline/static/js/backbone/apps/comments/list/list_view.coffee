@Gasoline.module "CommentsApp.List", (List, App, Backbone, Marionette, $, _) ->
    
    class List.LayoutView extends App.Views.LayoutView
        template: "comments/list/templates/list_layout"
        tagName: "div"
        className: "comment-timeline"
        regions:
            commentsRegion: "#comments-timeline-region"
            commentsActionsRegion: "#comments-timeline-actions-region"

    class List.Comment extends App.Views.FormView
        template: "comments/list/templates/_comment"
        tagName: "div"
        className: "comment-item"

        ui:
            edit: '#comment-edit'
            delete: '#comment-delete'
            cancel: '#comment-edit-form-cancel'
            commentEditForm: '.comment-edit-form'
            commentView: '.comment-view'
            content: '[name="content"]'

        events:
            "click @ui.edit" : ->
                console.log "edit clicked", @model, @
                @trigger "edit:comment"
            "click @ui.delete" : ->
                console.log "delete clicked", @model
                @model.destroy()
            "click @ui.cancel" : ->
                console.log "cancel clicked", @model
                @trigger "show:comment"

        initialize: (options) ->
            super options

            # show comment, hide form
            @listenTo @, "show:comment" : ->
                @ui.commentEditForm.hide()
                @ui.commentView.show()
            # show comment edit form, hide comment view
            @listenTo @, "edit:comment" : ->
                @ui.commentView.hide()
                @ui.commentEditForm.show()

        createModel: ->
            @model

        updateModel: ->
            @model.set
                content: @ui.content.val()
                author: @model.get('author').name or @model.get('author')

        onSuccess: (model) ->
            console.log "success save", model
            @trigger "show:comment"


    class List.Comments extends App.Views.CompositeView
        template: "comments/list/templates/_comments"
        childView: List.Comment
    
    class List.NewComment extends App.Views.FormView
        template: "comments/list/templates/_new_comment"

        ui:
            content: '[name="content"]'

        initialize: (options) ->
            @space = options.space
            @doc = options.doc
            @collection = options.collection
            super options

        createModel: ->
            @model = App.request "comments:entities:empty", @space, @doc

        updateModel: ->
            @model.set
                author: "doe"
                content: @ui.content.val()

            @listenTo @model, "sync", (model, resp, options) =>
                @collection.add model

        onSuccess: (model) ->
            App.vent.trigger "comment:saved", model
