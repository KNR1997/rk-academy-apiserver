import uuid

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from academy.app.permissions.base import ROLE, ROLE_PERMISSIONS


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False, db_index=True, primary_key=True
    )
    username = models.CharField(max_length=128, blank=True, null=True)
    # user fields
    mobile_number = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, null=True, blank=True, unique=True)
    # notification_email = models.CharField(max_length=255, null=True, blank=True, unique=True)

    # identity
    display_name = models.CharField(max_length=255, default="")
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)

    # tracking metrics
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Modified At")

    # the is' es
    is_superuser = models.BooleanField(default=False)
    is_managed = models.BooleanField(default=False)
    is_password_expired = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_password_autoset = models.BooleanField(default=False)

    role = models.PositiveSmallIntegerField(
        choices=[(r.value, r.name) for r in ROLE],
        default=ROLE.GUEST.value,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "users"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.username} <{self.email}>"

    @property
    def permissions(self) -> list[str]:
        return ROLE_PERMISSIONS.get(ROLE(self.role), [])

    @property
    def role_name(self) -> str:
        return ROLE(self.role).name.lower()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def save(self, *args, **kwargs):
        self.email = self.email.lower().strip() if self.email else None
        self.mobile_number = self.mobile_number

        # if self.token_updated_at is not None:
        #     self.token = uuid.uuid4().hex + uuid.uuid4().hex
        #     self.token_updated_at = timezone.now()

        # if not self.display_name:
        #     self.display_name = (
        #         self.email.split("@")[0]
        #         if len(self.email.split("@"))
        #         else "".join(random.choice(string.ascii_letters) for _ in range(6))
        #     )

        if self.is_superuser:
            self.is_staff = True

        super(User, self).save(*args, **kwargs)
