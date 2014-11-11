@Gasoline.module "ACLApp.List", (List, App, Backbone, Marionette, $, _) ->

    class List.LayoutView extends App.Views.LayoutView
        template: "acl/list/list_layout"
        regions:
            panelRegion:    "#panel-region"
            aclRegion:      "#acl-region"
            newAceRegion:   "#new-ace-region"

        ui:
            newUser: '#new-user-ace-button'
            newGroup: '#new-group-ace-button'
            newAny: '#new-any-ace-button'

        events:
            "click @ui.newUser" : -> @trigger "new:ace:clicked", "user"
            "click @ui.newGroup" : -> @trigger "new:ace:clicked", "group"
            "click @ui.newAny" : -> @trigger "new:ace:clicked", "ANY"

        dialog: ->
            title: => "ACL"
            size: "lg"

    class List.ACE extends App.Views.ItemView
        template: "acl/list/_ace"
        tagName: "tr"

        modelEvents:
            "updated" : "render"

        ui:
            delete: '#delete'

        triggers:
            "click @ui.delete" : "delete:ace:clicked"

        initialize: ->
            @events = {} if not @events
            @registerEvents()

        # register events for each permissions
        registerEvents: ->
            # add event for each permissions keys
            @model.permissionsKeys.forEach (key) =>
                @events["click ##{key}"] = ->
                    @togglePermission key

            # update events
            @delegateEvents()

        # toggle permission value and save
        togglePermission: (key) ->
            if @model.attributes.permissions[key] == 'ALLOW'
                @model.attributes.permissions[key] = 'DENY'
            else if @model.attributes.permissions[key] == 'DENY'
                @model.attributes.permissions[key] = ''
            else
                @model.attributes.permissions[key] = 'ALLOW'
            @model.save()

        templateHelpers: ->
            user: @user()
            group: @group()
            allow: 'ALLOW'
            deny: 'DENY'
            permissionsKeys: @model.permissionsKeys

        user: ->
            @model.get('predicate').split(':')[1] if @model.get('predicate').search('u:') == 0

        group: ->
            @model.get('predicate').split(':')[1] if @model.get('predicate').search('g:') == 0

    class List.ACL extends App.Views.CompositeView
        template: "acl/list/_acl"
        childView: List.ACE
        childViewContainer: "tbody"

    class List.Panel extends App.Views.ItemView
        template: "acl/list/_panel"
        className: "row"
