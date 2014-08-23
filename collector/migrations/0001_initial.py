# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Contest'
        db.create_table('collector_contest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('probs_names', self.gf('collector.separatedvaluesfield.SeparatedValuesField')(max_length=511)),
        ))
        db.send_create_signal('collector', ['Contest'])

        # Adding model 'Region'
        db.create_table('collector_region', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.CharField')(null=True, blank=True, max_length=255, default='')),
        ))
        db.send_create_signal('collector', ['Region'])

        # Adding model 'MassRegionResults'
        db.create_table('collector_massregionresults', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['collector.Region'])),
            ('contest', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['collector.Contest'], default=1)),
            ('raw', self.gf('django.db.models.fields.TextField')()),
            ('applied', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('collector', ['MassRegionResults'])

        # Adding model 'Result'
        db.create_table('collector_result', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('contest', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['collector.Contest'], default=1)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['collector.Region'])),
            ('grade', self.gf('django.db.models.fields.CharField')(null=True, blank=True, max_length=255)),
            ('probs_scores', self.gf('collector.separatedvaluesfield.SeparatedValuesField')(max_length=511)),
            ('score', self.gf('django.db.models.fields.IntegerField')()),
            ('mass', self.gf('django.db.models.fields.related.ForeignKey')(null=True, blank=True, to=orm['collector.MassRegionResults'])),
        ))
        db.send_create_signal('collector', ['Result'])


    def backwards(self, orm):
        # Deleting model 'Contest'
        db.delete_table('collector_contest')

        # Deleting model 'Region'
        db.delete_table('collector_region')

        # Deleting model 'MassRegionResults'
        db.delete_table('collector_massregionresults')

        # Deleting model 'Result'
        db.delete_table('collector_result')


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '255', 'default': "''"})
        },
        'collector.result': {
            'Meta': {'object_name': 'Result'},
            'contest': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['collector.Contest']", 'default': '1'}),
            'grade': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mass': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['collector.MassRegionResults']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'probs_scores': ('collector.separatedvaluesfield.SeparatedValuesField', [], {'max_length': '511'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['collector.Region']"}),
            'score': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['collector']