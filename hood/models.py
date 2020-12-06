from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.base_user import BaseUserManager


# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        print("email...",email)
        print("password...",password)
        return self._create_user(email, password=password, **extra_fields)

class Neighborhood(models.Model):
    name = models.CharField(max_length=100)
    hood_image =CloudinaryField('image',  null=True) 
    location = models.CharField(max_length=100, null=True)
    count = models.IntegerField()
    police = models.CharField(max_length=100)
    police_department_address = models.CharField(max_length=100)
    health = models.CharField(max_length=100)
    health_department_address = models.CharField(max_length=100)


    def __str__(self):
        return f' {self.name} Neighborhood'


    def create_neighborhood(self):
        self.save()

    def delete_neighborhood(self):
        self.delete()
                   
    @classmethod
    def find_neighborhood_by_id(cls,id):
        neighborhood_result = cls.objects.get(id=id)
        return neighborhood_result
 
    @classmethod
    def update_occupants(cls,current_value,new_value):
        fetched_object = cls.objects.filter(count=current_value).update(count=new_value)
        return fetched_object

    @classmethod
    def update_neighborhood(cls,current_value,new_value):
        fetched_object = cls.objects.filter(count=current_value).update(count=new_value)
        return fetched_object


    @classmethod
    def retrieve_all(cls):
        all_objects = Neighborhood.objects.all()
        for item in all_objects:
            return item
 
class Business(models.Model):
# specifying business choices  
    BUSINESS_CHOICES = (
        ("1", "Banking and Finance"), 
        ("2", "Food and Drinks"), 
        ("3", "Groceries"), 
        ("4", "Beauty parlour"), 
        ("5", "Barber shop"), 
        ("6","Electronics")
        )
    business_name = models.CharField(max_length=100, unique= True)
    business_user = models.ForeignKey(User,on_delete=models.CASCADE)
    business_image =CloudinaryField('image', null=True) 
    business_category = models.CharField( 
        max_length = 20, 
        choices = BUSINESS_CHOICES, 
        default = '1'
        )
    business_location = models.ForeignKey(Neighborhood, null=True, on_delete=models.CASCADE)
    phone_number = models.IntegerField(null=True)
    business_email = models.EmailField(max_length=100, unique= True) 

    
    def create_business(self):
        self.save()

    def delete_business(self):
        self.delete()

    
    @classmethod              
    def find_business_by_id(cls,id):
        business_result = cls.objects.get(id=id)
        return business_result

    
    @classmethod
    def update_business(cls,current_value,new_value):
        fetched_object = cls.objects.filter(business_name=current_value).update(business_name=new_value)
        return fetched_object


    def search_by_business(cls,search_term):
        search_result = cls.objects.filter(business_name__icontains=search_term)
        return search_result   


class Profile(models.Model):
    profile_pic =CloudinaryField('image')       
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    neighborhood = models.ForeignKey(Neighborhood,null=True, related_name='population', on_delete=models.CASCADE)    
    email_address = models.EmailField(max_length=150, null=True)
    status = models.BooleanField(null=True)
    
    def __str__(self):
        return self.user.username
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)
    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()

    @property
    def image(self):
        if self.profile_pic and hasattr(self.profile_pic, 'url'):
            return self.profile_pic.url

    @classmethod
    def search_by_username(cls,search_term):
        search_result = cls.objects.filter(user__username__icontains=search_term)
        return search_result

    @classmethod
    def update_profile(cls,id,value):
        cls.objects.filter(id=id).update(user_id = new_user)

    
    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    def __str__(self):
        return self.user

    def create_user_profile(sender, instance, created, **kwargs):
	    if created:
		    Profile.objects.create(user=instance)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        print("email...",email)
        print("password...",password)
        return self._create_user(email, password=password, **extra_fields)
        
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
        
        
        post_save.connect(create_user_profile, sender=User)
        post_save.connect(save_user_profile, sender=User)




class Post(models.Model):
    post_title = models.CharField(max_length=100, null=True)
    post_image = CloudinaryField('image')
    description =  models.CharField(max_length=70)    
    categories = models.CharField(max_length=70)
    time_created =  models.DateTimeField(auto_now=True, null=True)
    location = models.ForeignKey(Neighborhood, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.description
        
