from django.db import models
from django.contrib.auth import get_user_model


class Companies(models.Model):
    name = models.CharField(max_length=250, blank=False)
    short_name = models.CharField(max_length=50, blank=False)
    abbreviation = models.CharField(max_length=10, blank=False)
    description = models.TextField(blank=True)
    securities_list = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=100, blank=True)
    zse_mark = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class ListItems(models.Model):
    report_name = models.CharField(max_length=250, blank=False)
    title = models.CharField(max_length=250, blank=False)
    stripped_title = models.CharField(max_length=250, blank=False)
    aop_mark = models.IntegerField(blank=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class GfiHeaders(models.Model):
    load_date = models.DateTimeField(auto_now_add=True, blank=True)
    original_file_name = models.CharField(max_length=250)
    file_name = models.CharField(max_length=250)
    company = models.ForeignKey(Companies, on_delete=models.PROTECT, blank=True, null=True)
    company_name = models.CharField(max_length=250, blank=True)
    user = models.ForeignKey(get_user_model(), models.PROTECT, null=True)
    year = models.IntegerField(blank=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return "{company}, {year}".format(company=self.company.name, year=self.year)


class GfiDetails(models.Model):
    header = models.ForeignKey(GfiHeaders, on_delete=models.PROTECT, blank=False, null=False)
    item = models.ForeignKey(ListItems, on_delete=models.PROTECT, blank=False, null=False)
    value = models.IntegerField(default=0)
    value_last_year = models.IntegerField(default=0)
    description = models.TextField(blank=True)

    def __str__(self):
        return "{header}-{detail}".format(header=self.header, detail=self.item.aop_mark)


class Securities(models.Model):
    mark = models.CharField(max_length=20, blank=False, null=False)
    company = models.ForeignKey(Companies, on_delete=models.PROTECT, blank=False, null=False)
    isin = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField(blank=True)
    issued_number = models.IntegerField(default=0)
    nominal_value = models.DecimalField(max_digits=12, decimal_places=2)
    enlistment_date = models.DateTimeField(auto_now_add=True, blank=True)
    zse_mark = models.CharField(max_length=50, blank=True)


class IndicatorTypes(models.Model):
    mark = models.CharField(max_length=10, blank=False, null=False)
    name = models.CharField(max_length=250, blank=False, null=False)
    description = models.TextField(blank=True)
    formula = models.TextField(blank=True)


class Indicators(models.Model):
    company = models.ForeignKey(Companies, on_delete=models.PROTECT, blank=False, null=False)
    indicator_type = models.ForeignKey(IndicatorTypes, on_delete=models.PROTECT, blank=False, null=False)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    calc_date = models.DateTimeField(auto_now_add=True, blank=True)
