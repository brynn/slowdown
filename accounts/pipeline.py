from django.shortcuts import redirect

from social.pipeline.partial import partial

import logging
log = logging.getLogger(__name__)


@partial
def require_email(strategy, details, user=None, is_new=False, *args, **kwargs):
    if user and user.email:
        return
    elif is_new and not details.get('email'):
        if strategy.session_get('saved_email'):
            details['email'] = strategy.session_pop('saved_email')
        if strategy.session_get('frequency'):
            details['frequency'] = strategy.session_pop('frequency')
        else:
            return redirect('require_email')
