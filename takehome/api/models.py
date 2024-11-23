from django.db import models
import uuid


class CustomUser(models.Model):
    # Extend the User model to include additional fields
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    mobile_number = models.CharField(max_length=15,
                                     unique=True)
    city = models.CharField(max_length=100)
    referral_code = models.CharField(max_length=8,
                                     unique=True,
                                     null=True,
                                     blank=True)
    referred_by = models.ForeignKey('self',
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    blank=True,
                                    related_name='referrals')

    def save(self, *args, **kwargs):
        # Generate referral code if not already present
        if not self.referral_code:
            self.referral_code = str(uuid.uuid4()).split('-')[0].upper()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.email


# Referral model to track referrer-referee relationship
class Referral(models.Model):
    referrer = models.ForeignKey(CustomUser,
                                 on_delete=models.CASCADE,
                                 related_name='referrals_made')
    referee = models.ForeignKey(CustomUser,
                                on_delete=models.CASCADE,
                                related_name='referrals_received')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.referrer.email} referred {self.referee.email}"

