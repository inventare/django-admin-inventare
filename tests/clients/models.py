from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=250)
    is_usable = models.BooleanField(null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'client'
        verbose_name_plural = 'clients'
