# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Comparison(models.Model):
    filename1 = models.TextField(blank=True, null=True)
    filename2 = models.TextField(blank=True, null=True)
    levenshtein = models.TextField(blank=True, null=True)  # This field type is a guess.
    jaccard = models.TextField(blank=True, null=True)  # This field type is a guess.
    jarowinkler = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'comparison'


class Samples(models.Model):
    sha_256 = models.TextField(primary_key=True, blank=True, null=False)
    malware_name = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    first_bytes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'samples'
