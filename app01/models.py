from django.db import models
'''
create table book(
        id int primary key auto_increment,
        title varchar(64) not null,
        state boolean not null,
        pub_date date not null,
        price decimal(20,5),
        publish varchar(32) not null
        
)
'''
# Create your models here.


class Book(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)
    state = models.BooleanField(default=True)
    pub_date = models.DateField()
    price = models.DecimalField(max_digits=20,decimal_places=5)#最长20，小数5位
    publish = models.CharField(max_length=32)

class first_second(models.Model):
    first = models.CharField(max_length=255)
    second = models.CharField(primary_key=True, max_length=255)

    class Meta:
        managed = True
        db_table = 'first_second'

class second_third(models.Model):
    second = models.CharField(max_length=255)
    third = models.CharField(primary_key=True, max_length=255)

    class Meta:
        managed = True
        db_table = 'second_third'


class third_fourth(models.Model):
    third = models.CharField(max_length=255)
    fourth = models.CharField(primary_key=True, max_length=255)

    class Meta:
        managed = True
        db_table = 'third_fourth'

class fourth_firmname(models.Model):
    security_id = models.CharField(max_length=255, blank=True, null=True)
    firmname = models.CharField(max_length=255, blank=True, null=True)
    stock_id = models.CharField(primary_key=True, max_length=255)
    fourth = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'fourth_firmname'

class enterprise_sentiment(models.Model):
    click_num = models.IntegerField(blank=True, null=True)
    review_num = models.CharField(max_length=225, blank=True, null=True)
    opinion = models.CharField(max_length=255)
    date = models.CharField(primary_key=True,max_length=255)
    stock_id = models.CharField(max_length=255)
    vocabulary1 = models.CharField(max_length=255, blank=True, null=True)
    vocabulary2 = models.CharField(max_length=255, blank=True, null=True)
    enterprise_sentiment = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'enterprise_sentiment'
        unique_together = (('date', 'stock_id', 'opinion'),)

class element_contrib(models.Model):
    stock_id = models.CharField(primary_key=True, max_length=255)
    tot_stock = models.DecimalField(max_digits=8, decimal_places=7, blank=True, null=True)
    inc_rev = models.DecimalField(max_digits=8, decimal_places=7, blank=True, null=True)
    roa = models.DecimalField(max_digits=8, decimal_places=7, blank=True, null=True)
    his_creidt = models.DecimalField(max_digits=8, decimal_places=7, blank=True, null=True)
    volatility = models.DecimalField(max_digits=8, decimal_places=7, blank=True, null=True)
    scale = models.DecimalField(max_digits=8, decimal_places=7, blank=True, null=True)
    credit_change = models.DecimalField(max_digits=8, decimal_places=7, blank=True, null=True)
    new_credit = models.DecimalField(max_digits=8, decimal_places=7, blank=True, null=True)
    cash_liability = models.DecimalField(max_digits=8, decimal_places=7, blank=True, null=True)
    laysuit_num = models.DecimalField(max_digits=8, decimal_places=7, blank=True, null=True)
    sentiment = models.DecimalField(max_digits=8, decimal_places=7, blank=True, null=True)
    roe = models.DecimalField(max_digits=8, decimal_places=7, blank=True, null=True)
    pb = models.DecimalField(max_digits=8, decimal_places=7, blank=True, null=True)
    day_accpay = models.DecimalField(max_digits=8, decimal_places=7, blank=True, null=True)
    com_grade = models.DecimalField(max_digits=8, decimal_places=7, blank=True, null=True)
    day_inventory = models.DecimalField(max_digits=8, decimal_places=7, blank=True, null=True)
    cash_rev = models.DecimalField(max_digits=8, decimal_places=7, blank=True, null=True)
    income = models.DecimalField(max_digits=8, decimal_places=7, blank=True, null=True)
    eps_incre = models.DecimalField(max_digits=8, decimal_places=7, blank=True, null=True)
    beta = models.DecimalField(max_digits=8, decimal_places=7, blank=True, null=True)
    shareholder_num = models.DecimalField(max_digits=8, decimal_places=7, blank=True, null=True)
    liquidity_ratio = models.DecimalField(max_digits=8, decimal_places=7, blank=True, null=True)
    liquidity_asset = models.DecimalField(max_digits=8, decimal_places=7, blank=True, null=True)
    debt_asset = models.DecimalField(max_digits=8, decimal_places=7, blank=True, null=True)
    value = models.DecimalField(max_digits=8, decimal_places=7, blank=True, null=True)
    yield_field = models.DecimalField(db_column='yield', max_digits=8, decimal_places=7, blank=True, null=True)  # Field renamed because it was a Python reserved w.org

    staff_num = models.DecimalField(max_digits=8, decimal_places=7, blank=True, null=True)
    reg_cap = models.DecimalField(max_digits=8, decimal_places=7, blank=True, null=True)
    day_accrec = models.DecimalField(max_digits=8, decimal_places=7, blank=True, null=True)
    ps = models.DecimalField(max_digits=8, decimal_places=7, blank=True, null=True)
    credit_num = models.IntegerField(blank=True, null=True)
    credit_str = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'element_contrib'


class enterprise_data(models.Model):
    sec_id = models.CharField(primary_key=True, max_length=255)
    firmname = models.CharField(max_length=255, blank=True, null=True)
    stock_id = models.CharField(max_length=255)
    scale = models.IntegerField(blank=True, null=True)
    reg_cap = models.FloatField(blank=True, null=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    staff_num = models.IntegerField(blank=True, null=True)
    first = models.CharField(max_length=255, blank=True, null=True)
    second = models.CharField(max_length=255, blank=True, null=True)
    third = models.CharField(max_length=255, blank=True, null=True)
    fourth = models.CharField(max_length=255, blank=True, null=True)
    tot_stock = models.FloatField(blank=True, null=True)
    shareholder_num = models.IntegerField(blank=True, null=True)
    org_stock = models.FloatField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    pe = models.FloatField(blank=True, null=True)
    pb = models.FloatField(blank=True, null=True)
    ps = models.FloatField(blank=True, null=True)
    yield_field = models.FloatField(db_column='yield', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    volatility = models.FloatField(blank=True, null=True)
    beta = models.FloatField(blank=True, null=True)
    com_grade = models.FloatField(blank=True, null=True)
    income = models.FloatField(blank=True, null=True)
    roe = models.FloatField(blank=True, null=True)
    roa = models.FloatField(blank=True, null=True)
    inc_rev = models.FloatField(blank=True, null=True)
    cash_rev = models.FloatField(blank=True, null=True)
    debt_asset = models.FloatField(blank=True, null=True)
    liquidity_asset = models.FloatField(blank=True, null=True)
    liquidity_ratio = models.FloatField(blank=True, null=True)
    cash_liability = models.FloatField(blank=True, null=True)
    day_inventory = models.FloatField(blank=True, null=True)
    day_accpay = models.FloatField(blank=True, null=True)
    day_accrec = models.FloatField(blank=True, null=True)
    eps_incre = models.FloatField(blank=True, null=True)
    income_incre = models.FloatField(blank=True, null=True)
    new_credit = models.FloatField(blank=True, null=True)
    his_creidt = models.FloatField(blank=True, null=True)
    laysuit_num = models.FloatField(blank=True, null=True)
    credit_date = models.CharField(max_length=255, blank=True, null=True)
    credit_change = models.IntegerField(blank=True, null=True)
    credit_type = models.CharField(max_length=255, blank=True, null=True)
    sentiment = models.FloatField(blank=True, null=True)
    credit_num = models.IntegerField(blank=True, null=True)
    credit_str = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'enterprise_data'
        unique_together = (('sec_id', 'stock_id'),)

class user_info(models.Model):
    user = models.CharField(primary_key=True,max_length=255)
    age = models.IntegerField(null=True)
    nickname = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    institute = models.CharField(max_length=255)
    img_src = models.CharField(max_length=255)
