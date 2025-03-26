from django.db import models
from django.utils.safestring import mark_safe



# Create your models here.
# class admin_model(models.Model):
#     admin_id = models.IntegerField(max_length=5)
#     name = models.CharField(max_length=30)
#     email_id = models.EmailField(max_length=20)
#     password = models.CharField(max_length=15)
#
#     def __str__(self):
#         return self.name

gender_list = [
    ("male","Male"),
    ("female","Female"),
    ("other","Others"),
]


class user(models.Model):
    name = models.CharField(max_length=30)
    email_id = models.EmailField(null=True)
    mobile_no = models.IntegerField() #new field added
    # dob = models.DateField(null=True)
    # gender = models.CharField(choices=gender_list,max_length=6,null=True)
    citys = models.CharField(max_length=30,null=True)
    propic = models.ImageField(upload_to='users',null=True)
    password = models.CharField(max_length=15)


    def __str__(self):
        return self.name

    def user_photo(self):
        return mark_safe('<img src="{}" width="100px" height="100px"/>'.format(self.propic.url))

    user_photo.allow_tags = True

class city(models.Model):
    city_name = models.CharField(max_length=15)
    popular_place = models.ImageField(upload_to='city',null=True)

    def __str__(self):
        return self.city_name

    def admin_photo(self):
        return mark_safe('<img src="{}" width="100px" height="100px"'.format(self.popular_place.url))

    admin_photo.allow_tags = True

class category(models.Model): #new model added
    cat_name = models.CharField(max_length=20)

    def __str__(self):
        return self.cat_name

language_list = [
    ("engish","English"),
    ("gujarati","Gujarati"),
    ("hindi","Hindi")
]


class monument(models.Model):
    monument_name = models.CharField(max_length=30) #new field added
    name_gujarati = models.CharField(max_length=30)
    name_hindi = models.CharField(max_length=30)
    city_name = models.ForeignKey(city,on_delete=models.CASCADE)
    info_english  = models.TextField()
    info_gujarati = models.TextField()
    info_Hindi = models.TextField()
    charges = models.IntegerField()
    photo = models.ImageField(upload_to='photos',)
    category = models.ForeignKey(category,on_delete=models.CASCADE)
    address = models.TextField()
    address_Gujarati = models.TextField()
    address_hindi = models.TextField()
    contact_no = models.BigIntegerField()
    timing = models.CharField(max_length=30)
    days = models.CharField(max_length=30)
    # language = models.CharField(choices=language_list,max_length=30,null=True)
    map_link = models.TextField()


    def admin_photo(self):
        return mark_safe("<img src='{}' width='100'".format(self.photo.url))

    admin_photo.allow_tags = True

    def __str__(self):
        return self.monument_name

class monument_photos(models.Model):
    monument = models.ForeignKey(monument,on_delete=models.CASCADE)
    photos = models.ImageField(upload_to='monument photos')

    def admin_photo(self):
        return mark_safe('<img src="{}" width="100" height="100"'.format(self.photos.url))

    admin_photo.allow_tags = True

payment_category = [
    ("debit card","Debit Card"),
    ("credit card","Credit Card"),
    ("bank transfer","Bank Transfer"),
]

class payment(models.Model):
    user_name = models.ForeignKey(user,on_delete=models.CASCADE)
    guide_name = models.CharField(max_length=30,null=True)
    email = models.EmailField(null=True)
    phone = models.BigIntegerField(null=True)
    monument_name = models.ForeignKey(monument,on_delete=models.CASCADE,null=True)
    total = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=15,choices=payment_category)
    charges = models.IntegerField(null=True)
    guide_date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    booked_time = models.DateTimeField(auto_now_add=True, null=True)
    
    # receipt_id = models.IntegerField()


class feedback(models.Model):
    user_name = models.ForeignKey(user,on_delete=models.CASCADE)
    monument_name = models.ForeignKey(monument,on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()
    photo = models.ImageField(upload_to="users",null=True)

    def admin_photo(self):
        return mark_safe('<img src="{}" width="100px" height="100px"'.format(self.photo.url))

    admin_photo.allow_tags = True

audio_lang_category = [
    ("English","English"),
    ("Gujarati","Gujarati"),
    ("Hindi","Hindi"),
]

class audio(models.Model):
    monument_name = models.ForeignKey(monument,on_delete=models.CASCADE,unique=True)
    file_path_english= models.FileField(upload_to='files',null=True,blank=True)
    file_path_gujarati= models.FileField(upload_to='files',null=True,blank=True)
    file_path_hindi= models.FileField(upload_to='files',null=True,blank=True)
    # audio_language = models.CharField(max_length=10,choices=audio_lang_category)

    def admin_audio_english(self):
        return mark_safe("<input type='file'>".format(self.file_path_english.url))

    def admin_audio_gujarati(self):
        return mark_safe("<input type='file'>".format(self.file_path_gujarati.url))

    def admin_audio_hindi(self):
        return mark_safe("<input type='file'>".format(self.file_path_hindi.url))


    admin_audio_english .allow_tags = True
    admin_audio_gujarati.allow_tags = True
    admin_audio_hindi.allow_tags = True

class contact(models.Model):
    name = models.CharField(max_length=30)
    phone = models.BigIntegerField()
    email = models.EmailField(null=True)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)



