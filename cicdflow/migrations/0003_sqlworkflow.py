# Generated by Django 4.1.3 on 2023-04-03 05:34

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cicdflow', '0002_jiraworkflow_init_flag_alter_jiraworkflow_project'),
    ]

    operations = [
        migrations.CreateModel(
            name='SqlWorkflow',
            fields=[
                ('w_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='工单ID')),
                ('sql_index', models.IntegerField(default=0, verbose_name='升级序号')),
                ('sql_release_info', models.IntegerField(default=0, verbose_name='SQL版本信息')),
                ('w_status', models.CharField(max_length=64, verbose_name='工单状态')),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('workflow_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sql_workflow_name', to='cicdflow.jiraworkflow', to_field='summary', verbose_name='工单名称')),
            ],
            options={
                'db_table': 'sql_workflow',
                'ordering': ['workflow_name', 'sql_index'],
            },
        ),
    ]
