from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class ApolloApp(models.Model):
    cluster_name = models.CharField(verbose_name=_('ClusterName'), max_length=20, default='default')
    namespace_name = models.CharField(verbose_name=_('NamespaceName'), max_length=20, default='application')
    item_key = models.CharField(verbose_name=_('ItemKey'), max_length=30)
    item_value = models.TextField(verbose_name=_('ItemValue'), max_length=1000)
    item_comment = models.TextField(verbose_name=_('ItemComment'), max_length=200, blank=True)
    create_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(auto_now=True)

    belong_app = models.ForeignKey('ApolloInstance', on_delete=models.CASCADE, related_name='app')

    class Meta:
        db_table = 'apollo_app'
        ordering = ['-update_date']
    def __str__(self):
        return "NameSpace: %s Key: (%s)" % (self.namespace_name, self.item_key)

class ApolloInstance(models.Model):
    app_id = models.CharField(verbose_name=_('AppId'), max_length=50, primary_key=True)
    env = models.CharField(verbose_name=_('Env'), max_length=20)
    app_name = models.CharField(verbose_name=_('AppName'), max_length=50, blank=True)
    department = models.CharField(verbose_name=_('Department'), max_length=30)
    principal = models.CharField(verbose_name=_('Principal'), max_length=30)
    username = models.CharField(verbose_name=_('Username'), max_length=15)
    create_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'apollo_instance'
        ordering = ['-update_date']
    def __str__(self):
        return self.app_id

