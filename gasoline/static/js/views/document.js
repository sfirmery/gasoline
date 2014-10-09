var app = app || {};
app.views = app.views || {};

app.views.DocumentView = Backbone.View.extend({
    template: _.template( $( '#documentTemplate' ).html() ),

    el: '#content',

    tagName: 'div',
    displayTemplate: _.template( $( '#displayDocumentTemplate' ).html() ),
    editTemplate: _.template( $( '#editDocumentTemplate' ).html() ),

    events: {
        'click #document-edit-form-save': 'saveDocument',
        'click #document-display-link': 'displayDocument',
        'click #document-edit-link': 'editDocument',
        'click #document-history-link': 'historyDocument',

        'click #document-attachments-link': 'attachmentsDocument',
        'click #document-rights-link': 'rightsDocument',
        'click #document-links-link': 'linksDocument',
        'click #document-informations-link': 'informationsDocument',
    },

   initialize: function(model, mode) {
        this.model = model;
        this.mode = mode;
        var self = this;

        console.log('init document view', this.model);

        _.bindAll(this, 'render');
        this.model.bind('sync', this.render);

        this.model.fetch(
            {
                success: function() {
                    console.log('fetch model success', self.model);
                }
            },
            {data:{space: 'main'}}
        );
    },

    render: function() {
        console.log("enter render");
        this.$el.html( this.template( this.model.toJSON(), mode=this.mode ) );
        switch ( this.mode ) {
            case 'edit':
                console.log('init edit document view');
                this.renderEdit();
                break;
            default:
                console.log('init display document view');
                this.renderDisplay();
        };
        // define current url and add history entry
        app.gasolineRouter.navigate('document/' + this.mode + '/' + this.model.get('space') + '/' + this.model.get('id'));
    },

    renderDisplay: function() {
        console.log("enter renderDisplay");
        this.$('#document').html( this.displayTemplate( this.model.toJSON(), mode=this.mode ) );


        console.log('render tag view');
        this.tags = new app.collections.Tags(null, {doc: this.model});
        app.tagsView = new app.views.TagsView(this.model, this.tags);
        var self = this, tags = [];
        this.model.get('tags').forEach(function(tag) {
            tags.push({tag: tag, space: self.model.get('space'), doc: self.model.get('id')});
        })
        this.tags.add(tags);


        this.comments = new app.collections.Comments(null, {doc: this.model});
        console.log('render comment view', this.comments);

        app.commentsView = new app.views.CommentsView(this.model, this.comments);

        Backbone.Events.trigger('document:rendered');
    },

    renderEdit: function() {
        console.log("enter renderEdit");
        this.$('#document').html( this.editTemplate( this.model.toJSON(), mode=this.mode ) );
    },

    displayDocument: function() {
        this.mode = 'display';
        this.render();
    },

    editDocument: function() {
        this.mode = 'edit';
        this.render();
    },

    saveDocument: function(e) {
        console.log('try save document');

        e.preventDefault();

        var formData = {};
        var self = this;

        $( '#document-edit div' ).children( 'input, textarea' ).each( function( i, el ) {
            formData[ el.name ] = $( el ).val();
        });

        this.mode = 'display';
        this.model.set(formData);
        this.model.save();
    },

});
