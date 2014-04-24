import json
from django.db import IntegrityError
from django.http import HttpResponse
from django.views.generic.edit import BaseCreateView 
from django.views.generic.base import View 

class AjaxView(View):

	def dispatch(self, *args, **kwargs):
		if not self.request.is_ajax():
			return HttpResponse(
				json.dumps({'message': 'Invalid Request'}),	
				content_type='application/json', 
				status=400
			)
		return super(AjaxView, self).dispatch(*args, **kwargs)
	
	def success(self, data={}, status=200):
		return HttpResponse(
			json.dumps(data), 
			content_type='application/json',
			status=status
		)

	def fail(self, errors={}, status=400):
		return HttpResponse(
			json.dumps(errors),	
			content_type='application/json',
			status=status
		)

class AuthAjaxView(AjaxView):
	
	def dispatch(self, *args, **kwargs):
		if not self.request.user.is_authenticated():
			return HttpResponse(
				json.dumps({'message': 'Login Required'}),	
				content_type='application/json', 
				status=401
			)
		return super(AuthAjaxView, self).dispatch(*args, **kwargs)

class AjaxCreateView(BaseCreateView, AjaxView):

	def form_valid(self, form):
		data = {} 
		try:
			self.object = form.save()
			bundle = {
				'id': self.object.id 
			}
			data['object'] = bundle
			data['done'] = True
		except IntegrityError:
			return self.form_invalid(form)
		
		return self.success(data)

	def form_invalid(self, form):
		return self.fail(form.errors)

	def get_success_url(self, *args, **kwargs):
		return ''
