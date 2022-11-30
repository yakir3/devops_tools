from django.urls import path, re_path
from .views import (
    ApolloView, ApolloDetailView,
    ApolloInstanceList, ApolloInstanceDetail,
    ApolloAuthorized
)
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'apollo'

urlpatterns = [
    # apollo authorized
    re_path('^authorized/(?P<app_id>[\w-]+)$', ApolloAuthorized.as_view(), name='apollo_authrized'),

    # apollo instance object
    re_path('^instance/(?P<app_id>[\w-]+)$', ApolloInstanceDetail.as_view(), name='apollo_ins_detail'),
    re_path('^instance', ApolloInstanceList.as_view(), name='apollo_ins'),
    # apollo app object
    path('', ApolloView.as_view(), name='apollo_app'),
    re_path('^(?P<app_id>[\w-]+)$', ApolloDetailView.as_view(), name='apollo_app_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
