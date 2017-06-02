from django.db import models
from django.contrib.auth import get_user_model


class Companies(models.Model):
    name = models.CharField(max_length=250, blank=False)
    short_name = models.CharField(max_length=50, blank=False)
    abbreviation = models.CharField(max_length=10, blank=False)
    description = models.TextField(blank=True)


class ListItems(models.Model):
    year = models.IntegerField(blank=False)
    title = models.CharField(max_length=250, blank=False)
    stripped_title = models.CharField(max_length=250, blank=False)
    description = models.TextField(blank=True)


class GfiHeaders(models.Model):
    load_date = models.DateTimeField(auto_now_add=True, blank=True)
    original_file_name = models.CharField(max_length=250)
    file_name = models.CharField(max_length=250)
    company = models.ForeignKey(Companies, on_delete=models.PROTECT, blank=True, null=True)
    company_name = models.CharField(max_length=250, blank=True)
    user = models.ForeignKey(get_user_model(), models.PROTECT, blank=False, null=False)
    description = models.TextField(blank=True)


class GfiDetails(models.Model):
    header = models.ForeignKey(GfiHeaders, on_delete=models.PROTECT, blank=False, null=False)
    item = models.ForeignKey(ListItems, on_delete=models.PROTECT, blank=False, null=False)
    value = models.IntegerField(default=0)
    value_last_year = models.IntegerField(default=0)
    description = models.TextField(blank=True)    
