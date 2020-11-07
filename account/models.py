from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if(not email):
            raise ValueError("Email required!")
        if not username:
            raise ValueError("Username required!")
        
        user = self.model(
            username = username,
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, username, email, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user

class Account(AbstractBaseUser):
    email 			= models.EmailField(verbose_name="email", max_length=60, unique=True)
    username 		= models.CharField(max_length=30, unique=True)
    date_joined		= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login		= models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin		= models.BooleanField(default=False)
    is_active		= models.BooleanField(default=True)
    is_staff		= models.BooleanField(default=False)
    is_superuser	= models.BooleanField(default=False)

    followers       = models.ManyToManyField('self', related_name="u_followers", symmetrical=False)		
    following       = models.ManyToManyField('self', related_name="u_following", symmetrical=False)		

    USERNAME_FIELD 	= 'username'
    REQUIRED_FIELDS = ['email']

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

# class Follow(models.Model):
#     following = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='following')
#     follower = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='follower')
#     follow_time = models.DateTimeField(auto_now=True)

#     class Meta:
#         unique_together = (('following', 'follower'),)
    