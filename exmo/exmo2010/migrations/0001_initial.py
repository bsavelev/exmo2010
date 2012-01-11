# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'OpennessExpression'
        db.create_table('exmo2010_opennessexpression', (
            ('code', self.gf('django.db.models.fields.PositiveIntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='-', max_length=255)),
        ))
        db.send_create_signal('exmo2010', ['OpennessExpression'])

        # Adding model 'Monitoring'
        db.create_table('exmo2010_monitoring', (
            ('status', self.gf('django.db.models.fields.PositiveIntegerField')(default=6)),
            ('openness_expression', self.gf('django.db.models.fields.related.ForeignKey')(default=8, to=orm['exmo2010.OpennessExpression'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='-', max_length=255)),
        ))
        db.send_create_signal('exmo2010', ['Monitoring'])

        # Adding model 'MonitoringStatus'
        db.create_table('exmo2010_monitoringstatus', (
            ('status', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('start', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('monitoring', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exmo2010.Monitoring'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('exmo2010', ['MonitoringStatus'])

        # Adding unique constraint on 'MonitoringStatus', fields ['status', 'monitoring']
        db.create_unique('exmo2010_monitoringstatus', ['status', 'monitoring_id'])

        # Adding model 'Organization'
        db.create_table('exmo2010_organization', (
            ('monitoring', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exmo2010.Monitoring'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('keywords', self.gf('exmo.exmo2010.fields.TagField')(null=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('exmo2010', ['Organization'])

        # Adding unique constraint on 'Organization', fields ['name', 'monitoring']
        db.create_unique('exmo2010_organization', ['name', 'monitoring_id'])

        # Adding model 'Parameter'
        db.create_table('exmo2010_parameter', (
            ('accessible', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('code', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('monitoring', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exmo2010.Monitoring'])),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('weight', self.gf('django.db.models.fields.IntegerField')()),
            ('hypertext', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('topical', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('complete', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('keywords', self.gf('exmo.exmo2010.fields.TagField')(null=True)),
            ('document', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('image', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('exmo2010', ['Parameter'])

        # Adding unique constraint on 'Parameter', fields ['code', 'monitoring']
        db.create_unique('exmo2010_parameter', ['code', 'monitoring_id'])

        # Adding unique constraint on 'Parameter', fields ['name', 'monitoring']
        db.create_unique('exmo2010_parameter', ['name', 'monitoring_id'])

        # Adding M2M table for field exclude on 'Parameter'
        db.create_table('exmo2010_parameter_exclude', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('parameter', models.ForeignKey(orm['exmo2010.parameter'], null=False)),
            ('organization', models.ForeignKey(orm['exmo2010.organization'], null=False))
        ))
        db.create_unique('exmo2010_parameter_exclude', ['parameter_id', 'organization_id'])

        # Adding model 'Task'
        db.create_table('exmo2010_task', (
            ('status', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exmo2010.Organization'])),
            ('openness_cache', self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('exmo2010', ['Task'])

        # Adding unique constraint on 'Task', fields ['user', 'organization']
        db.create_unique('exmo2010_task', ['user_id', 'organization_id'])

        # Adding model 'Score'
        db.create_table('exmo2010_score', (
            ('accessible', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('documentComment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exmo2010.Task'])),
            ('complete', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('hypertext', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('topicalComment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('hypertextComment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('completeComment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('accessibleComment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('topical', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('found', self.gf('django.db.models.fields.IntegerField')()),
            ('document', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('parameter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exmo2010.Parameter'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('imageComment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('exmo2010', ['Score'])

        # Adding unique constraint on 'Score', fields ['task', 'parameter']
        db.create_unique('exmo2010_score', ['task_id', 'parameter_id'])

        # Adding model 'Claim'
        db.create_table('exmo2010_claim', (
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('close_user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='close_user', null=True, to=orm['auth.User'])),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='creator', to=orm['auth.User'])),
            ('score', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exmo2010.Score'])),
            ('close_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('open_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('exmo2010', ['Claim'])

        # Adding model 'UserProfile'
        db.create_table('exmo2010_userprofile', (
            ('notify_score_change', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal('exmo2010', ['UserProfile'])

        # Adding M2M table for field organization on 'UserProfile'
        db.create_table('exmo2010_userprofile_organization', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['exmo2010.userprofile'], null=False)),
            ('organization', models.ForeignKey(orm['exmo2010.organization'], null=False))
        ))
        db.create_unique('exmo2010_userprofile_organization', ['userprofile_id', 'organization_id'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'OpennessExpression'
        db.delete_table('exmo2010_opennessexpression')

        # Deleting model 'Monitoring'
        db.delete_table('exmo2010_monitoring')

        # Deleting model 'MonitoringStatus'
        db.delete_table('exmo2010_monitoringstatus')

        # Removing unique constraint on 'MonitoringStatus', fields ['status', 'monitoring']
        db.delete_unique('exmo2010_monitoringstatus', ['status', 'monitoring_id'])

        # Deleting model 'Organization'
        db.delete_table('exmo2010_organization')

        # Removing unique constraint on 'Organization', fields ['name', 'monitoring']
        db.delete_unique('exmo2010_organization', ['name', 'monitoring_id'])

        # Deleting model 'Parameter'
        db.delete_table('exmo2010_parameter')

        # Removing unique constraint on 'Parameter', fields ['code', 'monitoring']
        db.delete_unique('exmo2010_parameter', ['code', 'monitoring_id'])

        # Removing unique constraint on 'Parameter', fields ['name', 'monitoring']
        db.delete_unique('exmo2010_parameter', ['name', 'monitoring_id'])

        # Removing M2M table for field exclude on 'Parameter'
        db.delete_table('exmo2010_parameter_exclude')

        # Deleting model 'Task'
        db.delete_table('exmo2010_task')

        # Removing unique constraint on 'Task', fields ['user', 'organization']
        db.delete_unique('exmo2010_task', ['user_id', 'organization_id'])

        # Deleting model 'Score'
        db.delete_table('exmo2010_score')

        # Removing unique constraint on 'Score', fields ['task', 'parameter']
        db.delete_unique('exmo2010_score', ['task_id', 'parameter_id'])

        # Deleting model 'Claim'
        db.delete_table('exmo2010_claim')

        # Deleting model 'UserProfile'
        db.delete_table('exmo2010_userprofile')

        # Removing M2M table for field organization on 'UserProfile'
        db.delete_table('exmo2010_userprofile_organization')
    
    
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'exmo2010.claim': {
            'Meta': {'object_name': 'Claim'},
            'close_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'close_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'close_user'", 'null': 'True', 'to': "orm['auth.User']"}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'creator'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'score': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exmo2010.Score']"})
        },
        'exmo2010.monitoring': {
            'Meta': {'object_name': 'Monitoring'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '255'}),
            'openness_expression': ('django.db.models.fields.related.ForeignKey', [], {'default': '8', 'to': "orm['exmo2010.OpennessExpression']"}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '6'})
        },
        'exmo2010.monitoringstatus': {
            'Meta': {'unique_together': "(('status', 'monitoring'),)", 'object_name': 'MonitoringStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monitoring': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exmo2010.Monitoring']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'exmo2010.opennessexpression': {
            'Meta': {'object_name': 'OpennessExpression'},
            'code': ('django.db.models.fields.PositiveIntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '255'})
        },
        'exmo2010.organization': {
            'Meta': {'unique_together': "(('name', 'monitoring'),)", 'object_name': 'Organization'},
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('exmo.exmo2010.fields.TagField', [], {'null': 'True'}),
            'monitoring': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exmo2010.Monitoring']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'exmo2010.parameter': {
            'Meta': {'unique_together': "(('code', 'monitoring'), ('name', 'monitoring'))", 'object_name': 'Parameter'},
            'accessible': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'complete': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'document': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'exclude': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['exmo2010.Organization']", 'null': 'True', 'blank': 'True'}),
            'hypertext': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'keywords': ('exmo.exmo2010.fields.TagField', [], {'null': 'True'}),
            'monitoring': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exmo2010.Monitoring']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'topical': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'weight': ('django.db.models.fields.IntegerField', [], {})
        },
        'exmo2010.score': {
            'Meta': {'unique_together': "(('task', 'parameter'),)", 'object_name': 'Score'},
            'accessible': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'accessibleComment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'complete': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'completeComment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'document': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'documentComment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'found': ('django.db.models.fields.IntegerField', [], {}),
            'hypertext': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hypertextComment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'imageComment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'parameter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exmo2010.Parameter']"}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exmo2010.Task']"}),
            'topical': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'topicalComment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'exmo2010.task': {
            'Meta': {'unique_together': "(('user', 'organization'),)", 'object_name': 'Task'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'openness_cache': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exmo2010.Organization']"}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'exmo2010.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notify_score_change': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['exmo2010.Organization']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }
    
    complete_apps = ['exmo2010']