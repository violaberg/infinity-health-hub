from django.db import models


class Contact(models.Model):
    """Model for contact form"""
    name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=700)


    def __str__(self):
        return f"{self.name}"