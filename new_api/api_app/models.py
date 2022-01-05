from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import FileExtensionValidator

# Create your models here.


class User(AbstractUser):
    username = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self):
        return "{}".format(self.email)


class UserProfile(models.Model):
    variants = (("f", "female"), ("m", "male"), ("o", "other"))
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    city = CharField(
        max_length=50,
    )
    gender = models.CharField(max_length=50, choices=variants, null=True)


class DocumentRequest(models.Model):
    INITIATED_STATUS = 1
    RECEIVED_STATUS = 2
    STATUS_VARIANTS = (
        (INITIATED_STATUS, "initiated"),
        (RECEIVED_STATUS, "received"),
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="to_user_sent", on_delete=models.CASCADE
    )
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="from_user_received",
        on_delete=models.CASCADE,
    )
    time = models.DateTimeField(auto_now_add=True)
    status_request = models.PositiveSmallIntegerField(choices=STATUS_VARIANTS, default=INITIATED_STATUS)
    file = models.FileField(upload_to="media/", null=True, blank=True, )
 # validators =[FileExtensionValidator(allowed_extensions=['pdf'])]