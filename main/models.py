from django.db import models
from Account.models import MyUser
from django.db.models.signals import post_save , m2m_changed , post_delete
from django.dispatch import receiver
from datetime import datetime , timedelta



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



class Facility(models.Model):
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
    latitude = models.TextField(null=True,blank=True)
    longitude = models.TextField(null=True,blank=True)
    slug = models.CharField(max_length=255, unique=True)
    status = models.CharField(choices=STATUS_CHOICE, default='Inactive', max_length=255)
    score = models.FloatField(null=True,blank=True)
    phone = models.CharField(max_length=11,null=True,blank=True)
    mobile = models.CharField(max_length=11,null=True,blank=True)
    description = models.TextField()
    sex = models.CharField(choices=SEX_CHOICE, default='مرد', max_length=32,null=True,blank=True)
    famous = models.CharField(max_length=32, choices=FAMOUS_CHOICE, default='None',null=True,blank=True)
    category_id = models.ManyToManyField(Category,related_name='categories',blank=True,null=True)
    user_id = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True,blank=True)
    facility_id = models.ManyToManyField(Facility,related_name='facilities',blank=True,null=True)


    def __str__(self):
        return self.name + ' ' + self.address

    def save(self, *args, **kwargs):
        self.slug = self.name.replace(' ', '_')
        super(Gym, self).save(*args, **kwargs)


class Slid(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.TextField()
    gym_id = models.ForeignKey(Gym, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + ' ' + self.gym_id.name



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
    name = models.CharField(max_length=255,null=True,blank=True)
    day = models.CharField(max_length=255, choices=STATUS_DAY, default='simple')
    open = models.TimeField()
    close = models.TimeField()
    price = models.TextField(default='')
    gym_id = models.ForeignKey(Gym, on_delete=models.CASCADE)
    sans = models.CharField(max_length=32, null=True, blank=True, choices=STATUS_SANS)

    class Meta:
        unique_together = ('open','day','gym_id')

    def __str__(self):
        return str(self.open)+' '+self.day+' '+self.gym_id.name

class Group(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    user_id = models.ManyToManyField(MyUser, related_name='group', null=True, blank=True)
    gym_id = models.ManyToManyField(Gym,related_name='group',null=True,blank=True)

    def __str__(self):
        return self.name


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    user_id = models.ManyToManyField(MyUser, related_name='role', null=True, blank=True)

    def __str__(self):
        return self.name


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
    user_id = models.ManyToManyField(MyUser,related_name='myuser',null=True,blank=True)
    hour_id = models.ManyToManyField(Hour,related_name='hour',null=True,blank=True)
    gym_id = models.ManyToManyField(Gym, related_name='gym' , null=True,blank=True)
    group_id = models.ManyToManyField(Group,related_name='group',null=True,blank=True)

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
    myuser_id = models.ForeignKey(MyUser, on_delete=models.CASCADE,related_name='order')
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

from PIL import Image


class Coach_Profile(models.Model):
    id = models.AutoField(primary_key=True)
    job = models.CharField(max_length=255)
    department_name = models.CharField(max_length=255)
    text = models.TextField()
    picture = models.ImageField(upload_to='coach_pictures/',default='coach_pictures/avatar.png')
    user_id = models.ForeignKey(MyUser,related_name='coach' ,on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user_id.name + ' ' + self.job

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     img = Image.open(self.picture.path)
    #     output_size = (500, 500)
    #     img.thumbnail(output_size)
    #     img.save(self.picture.path)

class Training_Class(models.Model):
    SEX_CHOICE = (
        ('مرد', 'man'),
        ('زن', 'woman')
    )
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    text = models.TextField()
    date_start = models.DateTimeField()
    date_expire = models.DateTimeField()
    picture = models.ImageField(upload_to='training-class-pic/')
    coach_id = models.ForeignKey(Coach_Profile, on_delete=models.CASCADE,related_name='training_class')
    gym_id = models.ForeignKey(Gym, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    number_of_session = models.IntegerField()
    price = models.TextField()
    hour_id = models.ForeignKey(Hour, on_delete=models.CASCADE)
    slug = models.CharField(max_length=64, null=True, blank=True)
    user_id = models.ManyToManyField(MyUser,related_name='students',null=True,blank=True)
    sex = models.CharField(choices=SEX_CHOICE,default='مرد',max_length=32)



    def __str__(self):
        return self.name + ' ' + self.coach_id.user_id.name

    def save(self, *args, **kwargs):
        self.slug = self.name.replace(' ', '_')
        super(Training_Class, self).save(*args, **kwargs)


#
# @receiver(post_save,sender = Province)
# def create_city(sender,instance,created,**kwargs):
# 	if created:
# 		Province.objects.create(user_id = instance)
#




@receiver(post_save, sender=Training_Class)
def add_order(sender,instance,created, **kwargs):
    if created:
        start_date = datetime.date(instance.date_start)
        end_date = datetime.date(instance.date_expire)
        day = instance.hour_id.day
        if day == 'doshanbe':
            numday =  0
        elif day == 'seshanbe':
            numday = 1
        elif day == 'charshanbe':
            numday = 2
        elif day == 'panjshanbe' :
            numday= 3
        elif day == 'jome':
            numday = 4
        elif day == 'shanbe':
            numday = 5
        elif day == 'yeshanbe':
            numday == 6

        amir = True
        while(amir):
            if start_date <= end_date :

                if start_date.weekday() == numday:

                    Order.objects.create(myuser_id=instance.coach_id.user_id,status='Reserved',description='Training class',order_date=start_date,gym_id=instance.gym_id,hour_id=instance.hour_id,total_price=instance.price,paid_money=instance.price)
            else:
                amir = False

            start_date = start_date + timedelta(days=1)


@receiver(post_save,sender=Gym)
def add_group(sender,instance,created,**kwargs):
    if created:
        user = None
        User_role = None
        try:
            user = instance.user_id
            user_role = Role.objects.get(user_id=user)
            if user_role.name == 'آموزش پرورش':
                add_to = Group.objects.get(name='آموزش پرورش')
                add_to.gym_id.add(instance)
                add_to.save()
        except:
            pass
#
@receiver(m2m_changed,sender = Role.user_id.through)
def create_profile(sender,instance,action,reverse,pk_set,**kwargs):

    if action == "post_add":
        user = pk_set
        role = Role.objects.get(name='مربی')
        try:
            for use in user:
                m = MyUser.objects.get(pk=use)
                profile = Coach_Profile.objects.get(user_id=MyUser.objects.get(pk = use))

        except:
            for use in user:
                m = MyUser.objects.get(pk=use)
                profile = Coach_Profile.objects.create(user_id=MyUser.objects.get(pk=use))

    if action == "post_remove":

        user = pk_set

        try:
            for use in user:
                profile = Coach_Profile.objects.filter(user_id__pk=use)
                profile.delete()
        except:
            pass

@receiver(m2m_changed,sender = Role.user_id.through)
def add_to_gp(sender,instance,action,reverse,pk_set,**kwargs):

    if action == "post_add":
        user = pk_set
        role = Role.objects.get(name='آموزش پرورش')
        if instance.name == 'آموزش پرورش':
            for use in user:
                try:
                        group = Group.objects.get(name='آموزش و پرورش' ,user_id=MyUser.objects.get(pk = use))
                except:
                        group = Group.objects.get(name = 'آموزش و پرورش')
                        group.user_id.add(use)

    if action == "post_remove":

        user = pk_set

        try:
            for use in user:
                group = Group.objects.get(user_id__pk=use,name = 'آموزش و پرورش')
                group.user_id.remove(use)
                group.save()
        except:
            pass

# def toppings_changed(sender,**kwargs):
#     print('aaaaaaaaaaaaaaaaaaaa')
#
# m2m_changed.connect(toppings_changed, sender=Role.user_id)
# def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
#     print('sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss')
#     # print(action)
#     # print(instance.products.all())
#     # print(instance.total)
#     #if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
#     products = instance.products.all()
#     total = 0
#     for x in products:
#         total += x.price
#     if instance.subtotal != total:
#         instance.subtotal = total
#         instance.save()
#     print(total)
# m2m_changed.connect(m2m_changed_cart_receiver, sender=Role.user_id.through)
