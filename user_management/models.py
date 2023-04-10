from django.db import models


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission

class UserManager(BaseUserManager):
    def create_user(self, email,username,first_name,last_name,user_type, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email=email)

        user = self.model(
            email=email,username=username,first_name=first_name,last_name=last_name,user_type=user_type
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,username, password):
        user = self.create_user(email=email, username=username, password=password, first_name="a" , last_name="a", user_type="P")
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user
    
    

class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE = (
        ('P','Patient'),
        ('C','Counsellor')
    )
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    user_type = models.CharField(choices=USER_TYPE, max_length=1,default="P")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    def is_patient(self):
        return self.USER_TYPE == "P"
    
    def is_counsellor(self):
        return self.USER_TYPE == "C"
    
    groups = models.ManyToManyField(
        Group,
        related_name='auth_user_groups',
        blank=True,
        verbose_name=('groups'),
        help_text=('The groups this user belongs to. A user will '
                    'get all permissions granted to each of their '
                    'groups.'),
        )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='auth_user_permissions',
        blank=True,
        verbose_name=('user permissions'),
        help_text=('Specific permissions for this user.'),
        )
    def get_by_natural_key(self, username):
        return self.get(username=username)
    
    class Meta:
        db_table = 'user_db'
        ordering = ['-date_joined']
        verbose_name_plural = "Users"


