@Gasoline.module "CommentsApp.Edit", (Edit, App, Backbone, Marionette, $, _) ->
    
    class Edit.Comment extends App.Views.ItemView
        template: "comments/list/templates/_comment"
        tagName: "div"
        className: "comment-item"

        ui:
            save: '#comment-save'
            cancel: '#comment-cancel'

        events:
            "submit @ui.save" : ->
                console.log "save clicked", @model, @
                # App.vent.trigger "edit:comment", @
            "click @ui.cancel" : ->
                console.log "cancel clicked", @model
                # @model.destroy()
