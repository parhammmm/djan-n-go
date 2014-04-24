var Forms = module({}); 

var Forms.Views.Django = Backbone.View.extend({

	events: {
		'submit': onSubmit,
		'send': onSend,
		'change input': onChange,
	},

	onChange: function(e){
		console.log(here);
	},

	onSend: function(e){
		this.onSubmit(e);
	},

	onSubmit: function(e){
		e.preventDefault();
		$(selector+' input[type="submit"]').attr('disabled', true);

		var that = this;
		var url = this.$el.attr('action');
		var method = this.$el.attr('method');
		var data = this.$el.serializeObject();

		var request = {
			url: url, 
			type: method, 
			data: data,
			dataType: "json",
		};

		var ajax = $.ajax(request);

		ajax.success(function(response){
			that.onFormSuccess(response, request);
		});

		ajax.fail(function(response){
			that.onFormError(response, request);
		});

		return false;
	},

	onFormSuccess: function(response, request){
		this.trigger('success', response, request)
	},

	onFormError: function(response, request){
		var errors = JSON.parse(response.responseText);
		this.trigger('error', errors, response, request)
		this.showFormErrors(errors);
	},

	showFormErrors: function(errors){
		this.resetFormErrors();
		this.resetFormMessage();

		if(errors.message){
			this.$('.error').text(errors.message);
			this.$('.error').show();
		} else {
			_.each(errors, function(value, name){
				$('<div class="inline-error alert alert-error">'+value+'</div>').insertAfter('input[name="'+name+'"]');
			});
		}
	},

	showFormMessage: function(msg){
		this.resetFormErrors();
		this.$('.message').text(msg);
		this.$('.message').show();
	},

	resetFormMessage: function(){
		this.$('.message').text('');
		this.$('.message').hide();
	},

	resetFormErrors: function(){
		this.$('.inline-error').remove();
		this.$('.error').hide();
	},

	getContext: function(){
		var context = {};
		context['csrf'] = getCookie('csrftoken');
		context['form'] = this.form;
		return context;
	},

	render: function(extra_context){
		var rendered = this.renderTemplate();
		this.$el.html(rendered);
		return this;
	},

});
