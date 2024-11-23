from django.db import models
import uuid

def generate_referral_code():
    return str(uuid.uuid4())[:8].upper()

class CustomUser(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    referral_code = models.CharField(
        max_length=8, 
        unique=True, 
        default=generate_referral_code
    )
    referred_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='referrals'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'custom_user'

    def __str__(self):
        return self.email
