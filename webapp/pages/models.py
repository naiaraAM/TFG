# pages/models.py
from django.db import models

class Comparison(models.Model):
    id = models.AutoField(primary_key=True)
    filename1 = models.TextField(blank=True, null=True)
    filename2 = models.TextField(blank=True, null=True)
    levenshtein = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    jaccard = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    jarowinkler = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    arithmetic_mean = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    geometric_mean = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comparison'
        unique_together = [['filename1', 'filename2']]


class Samples(models.Model):
    sha_256 = models.TextField(primary_key=True, blank=True, null=False)
    malware_name = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    first_bytes = models.TextField(blank=True, null=True)
    num_sections = models.IntegerField(blank=True, null=True)
    compiler = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'samples'
