# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Region.exp_links'
        db.add_column('collector_region', 'exp_links',
                      self.gf('django.db.models.fields.TextField')(null=True, default='', blank=True),
                      keep_default=False)

        # Adding field 'Region.res_links'
        db.add_column('collector_region', 'res_links',
                      self.gf('django.db.models.fields.TextField')(null=True, default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Region.exp_links'
        db.delete_column('collector_region', 'exp_links')

        # Deleting field 'Region.res_links'
        db.delete_column('collector_region', 'res_links')


    models = {
        'collector.contest': {
            'Meta': {'object_name': 'Contest'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'probs_names': ('collector.separatedvaluesfield.SeparatedValuesField', [], {'max_length': '511'})
        },
        'collector.massregionresults': {
            'Meta': {'object_name': 'MassRegionResults'},
            'applied': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'contest': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['collector.Contest']", 'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raw': ('django.db.models.fields.TextField', [], {}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['collector.Region']"})
        },
        'collector.region': {
            'Meta': {'object_name': 'Region'},
            'exp_links': ('django.db.models.fields.TextField', [], {'null': 'True', 'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'res_links': ('django.db.models.fields.TextField', [], {'null': 'True', 'default': "''", 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '255', 'default': "''", 'blank': 'True'})
        },
        'collector.result': {
            'Meta': {'object_name': 'Result'},
            'contest': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['collector.Contest']", 'default': '1'}),
            'grade': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mass': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['collector.MassRegionResults']", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'probs_scores': ('collector.separatedvaluesfield.SeparatedValuesField', [], {'max_length': '511'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['collector.Region']"}),
            'score': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['collector']