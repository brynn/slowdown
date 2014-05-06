# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Twitter'
        db.create_table(u'accounts_twitter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'accounts', ['Twitter'])

        # Adding model 'Instagram'
        db.create_table(u'accounts_instagram', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'accounts', ['Instagram'])

        # Adding model 'UserProfile'
        db.create_table(u'accounts_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, null=True, blank=True)),
            ('frequency', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('next_email_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_email_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('surprise_day', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('surprise_time', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('lat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lon', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('remixing', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('zen', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('podcasts', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('voyeurism', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('appendix_t', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('appendix_i', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'accounts', ['UserProfile'])

        # Adding M2M table for field twitters on 'UserProfile'
        m2m_table_name = db.shorten_name(u'accounts_userprofile_twitters')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm[u'accounts.userprofile'], null=False)),
            ('twitter', models.ForeignKey(orm[u'accounts.twitter'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userprofile_id', 'twitter_id'])

        # Adding M2M table for field instagrams on 'UserProfile'
        m2m_table_name = db.shorten_name(u'accounts_userprofile_instagrams')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm[u'accounts.userprofile'], null=False)),
            ('instagram', models.ForeignKey(orm[u'accounts.instagram'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userprofile_id', 'instagram_id'])

        # Adding model 'Item'
        db.create_table(u'accounts_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('item_type', self.gf('django.db.models.fields.CharField')(default='RM', max_length=2)),
            ('image_url', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('image_link', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('text_link', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('audio', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('hash_code', self.gf('django.db.models.fields.CharField')(max_length=11, null=True, blank=True)),
        ))
        db.send_create_signal(u'accounts', ['Item'])


    def backwards(self, orm):
        # Deleting model 'Twitter'
        db.delete_table(u'accounts_twitter')

        # Deleting model 'Instagram'
        db.delete_table(u'accounts_instagram')

        # Deleting model 'UserProfile'
        db.delete_table(u'accounts_userprofile')

        # Removing M2M table for field twitters on 'UserProfile'
        db.delete_table(db.shorten_name(u'accounts_userprofile_twitters'))

        # Removing M2M table for field instagrams on 'UserProfile'
        db.delete_table(db.shorten_name(u'accounts_userprofile_instagrams'))

        # Deleting model 'Item'
        db.delete_table(u'accounts_item')


    models = {
        u'accounts.instagram': {
            'Meta': {'object_name': 'Instagram'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'accounts.item': {
            'Meta': {'object_name': 'Item'},
            'audio': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'hash_code': ('django.db.models.fields.CharField', [], {'max_length': '11', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_link': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'item_type': ('django.db.models.fields.CharField', [], {'default': "'RM'", 'max_length': '2'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'text_link': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'accounts.twitter': {
            'Meta': {'object_name': 'Twitter'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'accounts.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'appendix_i': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'appendix_t': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'frequency': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instagrams': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['accounts.Instagram']", 'null': 'True', 'blank': 'True'}),
            'last_email_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'next_email_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'podcasts': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'remixing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'surprise_day': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'surprise_time': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'twitters': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['accounts.Twitter']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'voyeurism': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'zen': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['accounts']