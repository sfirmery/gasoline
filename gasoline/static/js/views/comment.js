var app = app || {};
app.views = app.views || {};

app.views.CommentView = Backbone.View.extend({
    tagName: 'div',
    className: 'comment-item',
    template: _.template( $( '#commentTemplate' ).html() ),
    editTemplate: _.template( $( '#commentEditTemplate' ).html() ),
    mode: 'display',

    events: {
        'click #comment-edit': 'editComment',
        'click #comment-edit-form-save': 'saveComment',
        'click #comment-delete': 'deleteComment',
    },

   initialize: function(options) {
        console.log("initialize comment", options);
        this.model = options.model;
        this.doc = options.doc;

        _.bindAll(this, 'render');
        this.model.bind('sync', this.render);
    },

    render: function() {
        console.log("enter render comment");

        this.el.id = 'comment-' + this.model.id;
        switch ( this.mode ) {
            case 'edit':
                console.log('init edit comment view');
                this.renderEdit();
                break;
            default:
                console.log('init display comment view');
                this.renderDisplay();
        };
        return this;
    },

    renderDisplay: function() {
        this.$el.html( this.template( this.model.toJSON(), mode=this.mode ) );

        Backbone.Events.trigger('comment:rendered', this.el);
    },

    renderEdit: function() {
        this.$el.html( this.editTemplate( this.model.toJSON(), mode=this.mode ) );
    },

    displayComment: function() {
        this.mode = 'display';
        this.render();
    },

    editComment: function() {
        if (app.currentUser.get('name') == this.model.get('author').name) {
            this.mode = 'edit';
            this.render();
        }
        else {
            console.log("permission denied");
        };
    },

    saveComment: function(e) {
        console.log("enter save comment");

        e.preventDefault();

        var formData = {};

        $('#comment-edit-form div').children('input, textarea').each( function(i, el) {
            formData[ el.name ] = $( el ).val();
        });

        // force doc and space values
        formData['doc'] = this.doc.get('id');
        formData['space'] = this.doc.get('space');

        this.mode = 'display';
        this.model.set(formData);
        this.model.save();
    },

    deleteComment: function() {
        //Delete model
        this.model.destroy();

        //Delete view
        this.remove();
    },

});

app.views.CommentsView = Backbone.View.extend({
    el: '#comments',

    formTemplate: _.template( $('#commentFormTemplate').html() ),

    events: {
        'click #comment-add-form-add': 'addComment',
    },

   initialize: function(doc, collection) {
        console.log("init comment view");
        var self = this;
        this.collection = collection;
        this.doc = doc;

        this.listenTo( this.collection, 'add', this.renderSingleComment );
        this.listenTo( this.collection, 'reset', this.renderComments );

        this.collection.fetch({
            reset: true,
            success: function() {
                console.log("self.collection", self.collection);
            }
        });

    },

    renderComment: function(item) {
        var commentView = new app.views.CommentView({ model: item, doc: this.doc });
        this.$el.children('.comment-timeline-items').append( commentView.render().el );
        return commentView.el;
    },

    renderSingleComment: function(item) {
        var el = this.renderComment(item);

        Backbone.Events.trigger('comment:rendered', el);
    },

    renderComments: function() {
        this.$el.children('li').remove()
        this.collection.each(function( item ) {
            this.renderComment(item);
        }, this );

        this.$el.children('.comment-timeline-actions').append( this.formTemplate( {author: app.currentUser.toJSON()} ) );

        Backbone.Events.trigger('comment:rendered', this.el);
    },

    addComment: function( e ) {
        console.log("enter add comment");
        var self = this;

        e.preventDefault();

        var formData = {};
        // set doc and space values
        formData['doc'] = this.doc.get('id');
        formData['space'] = this.doc.get('space');

        $('#comment-add-form div').children('input, textarea').each( function(i, el) {
            if( $(el).val() != '' )
            {
                formData[el.name] = $(el).val();
            }
            $(el).val('');
        });

        this.collection.create(formData, { wait: true });
    },

});
