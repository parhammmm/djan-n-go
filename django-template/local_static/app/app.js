define([
  // Libs
  "jquery",
  "lodash",
  "backbone",
],

function($, _, Backbone) {
  // Put application wide code here
  
  return {
    // This is useful when developing if you don't want to use a
    // build process every time you change a template.
    //
    // Delete if you are using a different template loading method.
    fetchTemplate: function(path, done) {
      var JST = window.JST = window.JST || {};

      var templateDir = "static/app/templates/";
      path = templateDir+path+".html";

      if (!JST[path]) {
        // Fetch it asynchronously if not available from JST, ensure that
        // template requests are never cached and prevent global ajax event
        // handlers from firing.
        $.ajax({
          url: "/" + path,
          dataType: "text",
          cache: false,
          async: false,

          success: function(contents) {
            JST[path] = contents;
          }
        });
      }

      // Ensure a normalized return value.
      return JST[path];
    },

    // Create a custom object with a nested Views object
    module: function(additionalProps) {
      return _.extend({ Views: {} }, additionalProps);
    },

    // Keep active application instances appd under an app object.
    app: _.extend({}, Backbone.Events)
  };
});
