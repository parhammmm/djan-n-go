// Set the require.js configuration for your application.
require.config({
	// Initialize the application with the main application file
	deps: ["main"],

	paths: {
		// JavaScript folders
		libs: "../assets/js/libs",
		plugins: "../assets/js/plugins",
		vendor: "../assets/vendor",

		// Libraries
		jquery: "../assets/js/libs/jquery",
		lodash: "../assets/js/libs/lodash",
		backbone: "../assets/js/libs/backbone",
		mustache: "../assets/js/libs/mustache",
	},

	shim: {
		backbone: {
			deps: ["lodash", "jquery"],
			exports: "Backbone"
		},

		mustache: {
			exports: "Mustache"
		},
	}
});