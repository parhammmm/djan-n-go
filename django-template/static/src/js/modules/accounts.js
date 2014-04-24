// Example

var Accounts = module({}); 

Accounts.Views.Signup = Forms.Views.Django.extend ({

	template: 'accounts_signup',

	form: {
		'action': '/accounts/ajax/signup/',
		'method': 'post'
	},

});
