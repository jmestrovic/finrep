from django.db import models
from django.contrib.auth import get_user_model


class Companies(models.Model):
    name = models.CharField(max_length=250, blank=False)
    short_name = models.CharField(max_length=50, blank=False)
    abbreviation = models.CharField(max_length=10, blank=False, db_index=True)
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
    aop_mark = models.IntegerField(blank=False, db_index=True)
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
    is_revised = models.NullBooleanField(default=True)
    is_consolidated = models.NullBooleanField(default=True)
    period = models.CharField(max_length=20, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return "{company}, {year}".format(company=self.company.name, year=self.year)

    class Meta:
        indexes = [
            models.Index(fields=['company', 'year'], name='gfi_headers__company__year'),
            models.Index(fields=['year', 'company'], name='gfi_headers__year__company'),
        ]


class GfiDetails(models.Model):
    header = models.ForeignKey(GfiHeaders, on_delete=models.PROTECT, blank=False, null=False, db_index=True)
    item = models.ForeignKey(ListItems, on_delete=models.PROTECT, blank=False, null=False)
    value = models.IntegerField(default=0)
    value_last_year = models.IntegerField(default=0)
    description = models.TextField(blank=True)

    def __str__(self):
        return "{header}-{detail}".format(header=self.header, detail=self.item.aop_mark)


class Securities(models.Model):
    mark = models.CharField(max_length=20, blank=False, null=False, db_index=True)
    company = models.ForeignKey(Companies, on_delete=models.PROTECT, blank=False, null=False)
    isin = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField(blank=True)
    issued_number = models.IntegerField(default=0)
    nominal_value = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.TextField(max_length=10, blank=True, null=True)
    enlistment_date = models.DateTimeField(auto_now_add=True, blank=True)
    zse_mark = models.CharField(max_length=50, blank=True)
    security_type = models.CharField(max_length=1, blank=True)  # O - obveznica; D - dionica

    def __str__(self):
        return "{mark}".format(mark=self.mark)


class IndicatorTypes(models.Model):
    mark = models.CharField(max_length=10, blank=False, null=False, db_index=True)
    name = models.CharField(max_length=250, blank=False, null=False)
    description = models.TextField(blank=True)
    formula = models.TextField(blank=True)

    def __str__(self):
        return "{mark}".format(mark=self.mark)


class Indicators(models.Model):
    company = models.ForeignKey(Companies, on_delete=models.PROTECT, blank=False, null=False)
    indicator_type = models.ForeignKey(IndicatorTypes, on_delete=models.PROTECT, blank=False, null=False, db_index=True)
    value = models.DecimalField(max_digits=5, decimal_places=2, db_index=True)
    calc_date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return "{company} - {indicator} ({calc_date})".format(company=self.company, indicator=self.indicator, calc_date=self.calc_date)

    class Meta:
        indexes = [
            models.Index(fields=['company', 'calc_date'], name='indicators__company__calc_date'),
            models.Index(fields=['calc_date', 'company'], name='indicators__calc_date__company'),
        ]


class StockIndexTypes(models.Model):
    mark = models.CharField(max_length=50, blank=False, null=False, db_index=True)
    name = models.CharField(max_length=250, blank=False, null=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return "{mark}".format(mark=self.mark)


class StockIndexMembers(models.Model):
    stock_index = models.ForeignKey(StockIndexTypes, on_delete=models.PROTECT, blank=False, null=False, db_index=True)
    security = models.ForeignKey(Securities, on_delete=models.PROTECT, blank=False, null=False, db_index=True)
    index_type = models.CharField(max_length=1, blank=True)  # O - obveznički; D - dionički
    free_float_factor = models.DecimalField(max_digits=12, decimal_places=2)
    weight_facor = models.DecimalField(max_digits=12, decimal_places=8)
    weight_facor = models.DecimalField(max_digits=12, decimal_places=4)
    description = models.TextField(blank=True)

    def __str__(self):
        return "{stock_index}".format(stock_index=self.stock_index)


class SecurityPrices(models.Model):
    date = models.DateTimeField(auto_now_add=False, blank=False)
    security = models.ForeignKey(Securities, on_delete=models.PROTECT, blank=False, null=False, db_index=True)
    last_price = models.DecimalField(max_digits=12, decimal_places=2, blank=False)
    change_pct = models.DecimalField(max_digits=7, decimal_places=4, blank=True)
    open_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    high_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    low_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    average_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    volume = models.IntegerField(blank=True)
    turnover = models.DecimalField(max_digits=20, decimal_places=2, blank=True)

    def __str__(self):
        return "{security} ({date}): {price}".format(security=self.security, date=self.date, price=self.price)


class SecurityPricesHistory(models.Model):
    date = models.DateTimeField(auto_now_add=False, blank=False)
    security = models.ForeignKey(Securities, on_delete=models.PROTECT, blank=False, null=False)
    last_price = models.DecimalField(max_digits=12, decimal_places=2, blank=False)
    closing_price = models.DecimalField(max_digits=12, decimal_places=2, blank=False)
    change_pct = models.DecimalField(max_digits=7, decimal_places=4, blank=True)
    open_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    high_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    low_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    average_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    volume = models.IntegerField(blank=True)
    turnover = models.DecimalField(max_digits=20, decimal_places=2, blank=True)

    def __str__(self):
        return "{security} ({date}): {price}".format(security=self.security, date=self.date, price=self.price)

    class Meta:
        indexes = [
            models.Index(fields=['date', 'security'], name='sec_pric_hist__date__security'),
            models.Index(fields=['security', 'date'], name='sec_pric_hist__security__date'),
        ]
