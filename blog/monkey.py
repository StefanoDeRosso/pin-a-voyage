from social import utils
from social.exceptions import InvalidEmail

from django.core import signing
from django.core.signing import BadSignature
from django.contrib.sessions.models import Session
from django.conf import settings

def partial_pipeline_data(backend, user=None, *args, **kwargs):
	data = backend.strategy.request_data()
	if 'signature' in data:
		try:
			signed_details = signing.loads(data['signature'], key=settings.EMAIL_SECRET_KEY)
			session = Session.objects.get(pk=signed_details['session_key'])
		except BadSignature, Session.DoesNotExist:
			raise InvalidEmail(backend)
		
		session_details = session.get_decoded()
		backend.strategy.session_set('email_validation_address', session_details['email_validation_address'])
		backend.strategy.session_set('next', session_details.get('next'))
		backend.strategy.session_set('partial_pipeline', session_details['partial_pipeline'])
		backend.strategy.session_set(backend.name + '_state', session_details.get(backend.name + '_state'))
		backend.strategy.session_set(backend.name + 'unauthorized_token_name',
									session_details.get(backend.name + 'unauthorized_token_name'))
									
	partial = backend.strategy.session_get('partial_pipeline', None)
	if partial:
		idx, backend_name, xargs, xkwargs = \
			backend.strategy.partial_from_session(partial)
		if backend_name == backend.name:
			kwargs.setdefault('pipeline_index', idx)
			if user:  # don't update user if it's None
				kwargs.setdefault('user', user)
			kwargs.setdefault('request', backend.strategy.request_data())
			xkwargs.update(kwargs)
			return xargs, xkwargs
		else:
			backend.strategy.clean_partial_pipeline()
utils.partial_pipeline_data = partial_pipeline_data
