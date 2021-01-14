from django.db import models
#import regex for email regexn
import re
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}

        #first and last name validator
        if len(post_data['username']) < 2:
            errors['username'] = "Userame should be at least 2 character"

        #email validator
        # EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # if not EMAIL_REGEX.match(post_data['email']):    # test whether a field matches the pattern            
        #     errors['email'] = "Invalid email address!"

        #check password length
        if len(post_data['password']) < 6:
            errors['password'] = "Password should be at least 6 chars"
        #check password == password useususu
        if (post_data['password'] != post_data['confirm_pass']):
            errors['confirm_pass'] = "Password didn't match."
        
        #check email uniquenes
        user_list = User.objects.filter(username=post_data['username'])
        if(len(user_list)>0):
            errors['username_uniqe'] = 'This user is already taken.'
        return errors

    def login_validator(self, post_data):
        errors = {}

        # #check email format
        # EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # if not EMAIL_REGEX.match(post_data['email']):    # test whether a field matches the pattern            
        #     errors['email'] = "Invalid email address!"

        user_list = User.objects.filter(username=post_data['username'])
        #check if email is in the db
        if len(user_list) == 0:
            errors['user_not_found'] = "User not in database!"
        else:
            #check password pw
            if bcrypt.checkpw(
                post_data['password'].encode(), 
                user_list[0].password.encode()
            ) != True:
                errors['password'] = 'Password Invalid'
        return errors


class HamburgerModel(models.Model):
    name = models.CharField(max_length=254)
    price = models.CharField(max_length=254)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(null=True, upload_to='hamburger_image/', blank=True)

class User(models.Model):
    username = models.CharField(max_length=254)
    password = models.CharField(max_length=254)
    phone = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #wish_uploaded
    # liked_wish = models.ManyToManyField('Wish', related_name='users_who_liked')
    #validation objects
    objects = UserManager()

class Order(models.Model):
    user_customer = models.ForeignKey('User', related_name='customer_orders', on_delete=models.CASCADE)
    address = models.CharField(max_length=254)
    ordered_items = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=32, default="pending")