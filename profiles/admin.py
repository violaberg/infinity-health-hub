from .models import UserProfile, NeuroDiversity, LifeStage
from django.contrib import admin

# Register your models here.
class NeuroDiversityAdmin(admin.ModelAdmin):
    list_display = (
        'neurodiversity',
        'description',
    )

class LifeStageAdmin(admin.ModelAdmin):
    list_display = (
        'lifestage',
        'description',
    )

class UserProfileAdmin(admin.ModelAdmin):
    """" User Profile admin """
    list_display = (
        "pk",
        "user",
        "alias",
        "image",
        "about_me",
        'is__approved',
        "lifestage",
        "IFAB",
        "neurodiversity",
    )

admin.site.register(UserProfile)
admin.site.register(NeuroDiversity)
admin.site.register(LifeStage)