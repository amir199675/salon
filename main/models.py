from django.db import models
from Account.models import MyUser
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class Province(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class City(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, unique=True)
    province_id = models.ForeignKey(Province, related_name='cities', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name + ' ' + self.province_id.name


class Area(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    city_id = models.ForeignKey(City, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name + ' ' + self.city_id.name + ' ' + self.city_id.province_id.name



class Category(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Gym(models.Model):
    STATUS_CHOICE = (
        ('Active', 'active'),
        ('Inactive', 'inactive'),
    )
    SEX_CHOICE = (
        ('مرد', 'man'),
        ('زن', 'woman')
    )
    FAMOUS_CHOICE = (
        ('Number_one', 'number_one'),
        ('Number_two', 'number_two'),
        ('None', 'none')
    )
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=64)
    area_id = models.ForeignKey(Area, on_delete=models.CASCADE)
    address = models.TextField()
    picture = models.ImageField(upload_to='gym_pictures/')
    latitude = models.TextField()
    longitude = models.TextField()
    slug = models.CharField(max_length=255, unique=True)
    status = models.CharField(choices=STATUS_CHOICE, default='Inactive', max_length=255)
    score = models.FloatField()
    phone = models.CharField(max_length=11)
    mobile = models.CharField(max_length=11)
    description = models.TextField()
    sex = models.CharField(choices=SEX_CHOICE, default='مرد', max_length=32)
    famous = models.CharField(max_length=32, choices=FAMOUS_CHOICE, default='None')
    category_id = models.ManyToManyField(Category,blank=True,null=True)

    def __str__(self):
        return self.name + ' ' + self.address


class Slid(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.TextField()
    gym_id = models.ForeignKey(Gym, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + ' ' + self.gym_id.name




class Gym_Category(models.Model):
    gym_id = models.ForeignKey(Gym, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.gym_id.name + ' ' + self.category_id.name


class Facility(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Hour(models.Model):
    STATUS_SANS = (
        ('One', 'one'),
        ('two', 'two'),
        ('Three', 'three'),
        ('Four', 'four'),
        ('Five', 'five'),
        ('Six', 'six'),
        ('seven', 'seven'),
        ('Eight', 'eight'),
        ('Nine', 'nine'),
        ('Ten', 'ten'),
        ('Eleven', 'eleven'),
        ('Twelve', 'twelve')

    )
    STATUS_DAY = (
        ('shanbe', 'shanbe'),
        ('yeshanbe', 'yeshanbe'),
        ('doshanbe', 'doshanbe'),
        ('seshanbe', 'seshanbe'),
        ('charshanbe', 'charshanbe'),
        ('panjshanbe', 'panjshanbe'),
        ('jome', 'jome'),
        ('simple', 'simple')
    )
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    day = models.CharField(max_length=255, choices=STATUS_DAY, default='simple')
    open = models.TimeField()
    close = models.TimeField()
    price = models.TextField(default='')
    gym_id = models.ForeignKey(Gym, on_delete=models.CASCADE)
    sans = models.CharField(max_length=32, null=True, blank=True, choices=STATUS_SANS)

    def __str__(self):
        return str(self.open)+' '+self.day+' '+self.gym_id.name


class Gym_Facility(models.Model):
    gym_id = models.ForeignKey(Gym, on_delete=models.CASCADE)
    facility_id = models.ForeignKey(Facility, on_delete=models.CASCADE)

    def __str__(self):
        return self.gym_id.name + ' ' + self.facility_id.name


class Group(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    user_id = models.ManyToManyField(MyUser, related_name='group', null=True, blank=True)

    def __str__(self):
        return self.name


class Group_MyUser(models.Model):
    myuser_id = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.myuser_id.name + ' ' + self.group_id.name


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    user_id = models.ManyToManyField(MyUser, related_name='role', null=True, blank=True)

    def __str__(self):
        return self.name


class Role_MyUser(models.Model):
    id = models.AutoField(primary_key=True)
    myuser_id = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return self.myuser_id.name + ' ' + self.role_id.name


class Comment(models.Model):
    STATUS_CHOICE = (
        ('Show', 'show'),
        ('Hidden', 'hidden'),
    )
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    gym_id = models.ForeignKey(Gym, on_delete=models.CASCADE)
    myuser_id = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    text = models.TextField()
    status = models.CharField(choices=STATUS_CHOICE, default='Hidden', max_length=255)

    def __str__(self):
        return self.myuser_id.name + ' ' + self.gym_id.name


class Favourite(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    gym_id = models.ForeignKey(Gym, on_delete=models.CASCADE)
    myuser_id = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.myuser_id.name


class Coupon(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    code = models.TextField()
    description = models.TextField()
    amount = models.FloatField()
    date_start = models.DateTimeField()
    date_expires = models.DateTimeField()
    usage_limit = models.IntegerField()
    minimum_amount = models.IntegerField()
    users = models.TextField()
    gym_id = models.ForeignKey(Gym, on_delete=models.CASCADE)
    groups = models.TextField()

    def __str__(self):
        return self.code


class Order(models.Model):
    STATUS_CHOICE = (
        ('Reserved', 'reserved'),
        ('Not Paid', 'not paid'),
        ('Reserving', 'reserving'),
        ('Expired', 'expired')
    )
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICE, default='Not Paid')
    description = models.TextField()
    myuser_id = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    gym_id = models.ForeignKey(Gym, on_delete=models.CASCADE)
    hour_id = models.ForeignKey(Hour, on_delete=models.CASCADE)
    order_date = models.DateField()
    total_price = models.TextField()
    paid_money = models.TextField()
    coupon_price = models.TextField(blank=True, null=True)
    coupon_id = models.ForeignKey(Coupon, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        unique_together = ('hour_id','order_date',)

    def __str__(self):
        return self.myuser_id.name + ' ' + self.status + ' ' + self.hour_id.day


class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    family_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    text = models.TextField()
    myuser_id = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.TextField(null=True, blank=True)
    email = models.EmailField()



class Coach_Profile(models.Model):
    id = models.AutoField(primary_key=True)
    job = models.CharField(max_length=255)
    department_name = models.CharField(max_length=255)
    text = models.TextField()
    picture = models.ImageField()
    user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user_id.name + ' ' + self.job


class Training_Class(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    date_start = models.DateTimeField()
    date_expire = models.DateTimeField()
    coach_id = models.ForeignKey(Coach_Profile, on_delete=models.CASCADE)
    gym_id = models.ForeignKey(Gym, on_delete=models.CASCADE)
    number_of_session = models.IntegerField()
    price = models.TextField()
    hour_id = models.ForeignKey(Hour, on_delete=models.CASCADE)
    slug = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.name + ' ' + self.coach_id.name


class Training_Class_MyUser(models.Model):
    training_class_id = models.ForeignKey(Training_Class, on_delete=models.CASCADE)
    myuser_id = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.myuser_id.name + ' ' + self.training_class_id.name

#
# @receiver(post_save,sender = Province)
# def create_city(sender,instance,created,**kwargs):
# 	if created:
# 		Province.objects.create(user_id = instance)
#
