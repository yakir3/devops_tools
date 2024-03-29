from django.db import models
# from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class CICDFlow(models.Model):
    email_title = models.CharField(verbose_name='邮件标题', primary_key=True, max_length=255)
    sql_info = models.JSONField(verbose_name='SVN 信息', blank=False, null=False)
    config_info = models.JSONField(verbose_name='配置文件信息', blank=False, null=False)
    apollo_info = models.JSONField(verbose_name='Apollo 信息', blank=False, null=False)
    project_info = models.JSONField(verbose_name='工程信息', blank=False, null=False)
    create_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'upgrade_flow'
        ordering = ['-update_date']
    def __str__(self):
        return "Upgrade Info: %s" % (self.email_title)

class CICDState(models.Model):
    email_title = models.ForeignKey('CICDFlow', on_delete=models.CASCADE, to_field='email_title', related_name='cicdstate')
    STATE_CHOICES = [
        (0, '执行成功/无需执行'),
        (1, '执行失败'),
        (2, '执行中，未返回状态'),
        (3, '待执行.'),
        (9, '未知状态')
    ]
    sql_state = models.IntegerField(verbose_name='SQL 升级执行状态', choices=STATE_CHOICES, default=9)
    # 配置与 Apollo 默认值为0
    config_state = models.IntegerField(verbose_name='配置文件升级执行状态', choices=STATE_CHOICES, default=9)
    apollo_state = models.IntegerField(verbose_name='Apollo 升级执行状态', choices=STATE_CHOICES, default=9)
    project_state = models.IntegerField(verbose_name='代码升级执行状态', choices=STATE_CHOICES, default=9)
    # flow_state 只保存 0/1/3 状态，对完整工作流是否执行的判断依据
    flow_state = models.IntegerField(verbose_name='工作流状态', choices=STATE_CHOICES, default=3)
    create_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'cicd_state'
        ordering = ['-update_date']
    def __str__(self):
        return "State: %s" % (self.email_title)

def init_data():
    return {
        'sql_init_flag': 0,
        'apollo_init_flag': 0,
        'config_init_flag': 0,
        'code_init_flag': 0
    }

class JiraWorkflow(models.Model):
    issue_key = models.CharField(verbose_name='编号key值', primary_key=True, max_length=64)
    issue_id = models.CharField(verbose_name='编号ID', max_length=32)
    summary = models.CharField(verbose_name='概要标题', blank=False, null=False, unique=True, max_length=255)
    status = models.CharField(verbose_name='当前状态', blank=False, null=False, max_length=64)
    project = models.CharField(verbose_name='归属项目', blank=True, null=False, max_length=16)
    priority = models.CharField(verbose_name='优先级', blank=False, null=False, max_length=16)
    labels = models.JSONField(verbose_name='标签', blank=True, null=True)
    environment = models.CharField(verbose_name='升级环境', blank=False, null=False, max_length=16)
    # issue_type = models.CharField(verbose_name='类型', blank=False, null=False, max_length=16, default='升级')

    sql_info = models.JSONField(verbose_name='SQL升级信息', blank=False, null=False, default=list)
    apollo_info = models.JSONField(verbose_name='Apollo升级信息', blank=False, null=False, default=list)
    # nacos_info = models.JSONField(verbose_name='Nacos升级信息', blank=False, null=False, default=list)
    config_info = models.JSONField(verbose_name='配置升级信息', blank=False, null=False, default=list)
    code_info = models.JSONField(verbose_name='代码升级信息', blank=False, null=False, default=list)
    # 初始化升级标志，0为首次升级，非0则为迭代升级
    init_flag = models.JSONField(verbose_name='初始化升级标志', blank=False, null=False, default=init_data)

    create_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'jira_workflow'
        ordering = ['-update_date']

    def __str__(self):
        return "Workflow Info: %s  %s" % (self.issue_key, self.summary)


class SqlWorkflow(models.Model):
    w_id = models.IntegerField(verbose_name='工单ID', primary_key=True)
    sql_id = models.CharField(verbose_name='SQL文件ID', max_length=32, default=0)
    sql_index = models.IntegerField(verbose_name='升级序号', default=0)
    sql_release_info = models.IntegerField(verbose_name='SQL版本信息', default=0)
    # workflow_name = models.ForeignKey(
    #     'JiraWorkflow', verbose_name='工单名称',on_delete=models.CASCADE, to_field='summary', related_name='sql_workflow_name')
    workflow_name = models.CharField(verbose_name='工单名称', max_length=256)
    w_status = models.CharField(verbose_name='工单状态', max_length=64)

    create_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sql_workflow'
        ordering = ['workflow_name', 'sql_index']

    def __str__(self):
        return str(self.sql_release_info)