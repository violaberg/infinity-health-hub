from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class NeuroDiversity(models.Model):
    """  A user profile model for maintaining default delivery information and order history   """
    neurodiversity = models.CharField(max_length=30)
    description = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Neurodiversities'

    def __str__(self):
        return str(self.neurodiversity)


class LifeStage(models.Model):
    lifestage = models.CharField(max_length=30)
    description = models.CharField(max_length=255)

    def __str__(self):
        return str(self.lifestage)


class UserProfile(models.Model):
    """  A user profile model to create and manage user profiles  """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    alias = models.CharField(max_length=30)
    about_me = models.CharField(max_length=255, blank=True)
    profile_image = models.ImageField(upload_to='images',
                                      default='placeholder.png')

    lifestage = models.ManyToManyField(LifeStage)
    IFAB = models.BooleanField(default=True)
    StillIdentifies = models.BooleanField(default=True)
    neurodiversity = models.ManyToManyField(NeuroDiversity)
    is_approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (str(self.alias) if self.alias else str(self.user.username))

    class Meta:
        """ order by recently created """
        ordering = ['-created_on']


# DMcC 23/04/24: Below is a signal this will ensure that whenever
# a User is created, a UserProfile is also created.
# Effectively this acts as a database trigger on save of User
# Note that this would normally sit in a separate signals.py file but
# incorporated here as relatively small code snippet


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """ Create or update the user profile """

    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()
