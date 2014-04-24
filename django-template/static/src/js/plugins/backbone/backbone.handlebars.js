(function() {

	var initialize = Backbone.View.prototype.initialize;

	Backbone.View.prototype.initialize = function(options){
		if (options.template)
			this.template = options.template; 

	    initialize.apply(this, arguments);
	};
	
	Backbone.View.prototype.getContext = function() {
		return {};
	};

	Backbone.View.prototype.getTemplate = function() {
		if (this.template){
			return Handlebars.templates[this.template]; 
		};
		return null;
	};

	Backbone.View.prototype.renderTemplate = function() {
		var context = this.getContext();
		var template = this.getTemplate(context);
		return (template) ? template(context) : null;
	};

})(window._, window.Backbone);
