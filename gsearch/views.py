from django.shortcuts import render
from django.conf import settings
from urllib.parse import urlparse
from django.contrib import messages

from globus_portal_framework.gsearch import (
    post_search, get_search_query, 
    get_search_filters, get_template,
    get_template_path
)

import logging
logger = logging.getLogger(__name__)

def dataset_search(request, index):
    context = {}
    query = get_search_query(request)
    if query:
        filters = get_search_filters(request)
        context['search'] = post_search(
            index, query, filters, request.user, request.GET.get('page', 1)
        )
        request.session['search'] = {
            'full_query': urlparse(request.get_full_path()).query,
            'query': query,
            'filters': filters,
            'index': index,
        }
        error = context['search'].get('error')
        if error:
            messages.error(request, error)
    
    context['datasets'] = {
        'numds': "800",
    }

    tvers = get_template_path('search.html', index=index)
    return render(request, get_template(index, tvers), context)
