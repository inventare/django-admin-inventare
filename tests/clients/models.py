from django.db import models

class Address(models.Model):
    street = models.CharField(max_length=140)

    def __str__(self):
        return self.street
    
    class Meta:
        verbose_name = 'address'
        verbose_name_plural = 'addresses'

class Client(models.Model):
    name = models.CharField(max_length=250, help_text='the client name')
    is_usable = models.BooleanField(null=True)
    birth_date = models.DateField()

    address = models.ForeignKey(Address, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'client'
        verbose_name_plural = 'clients'

class ClientPhone(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11)

    def __str__(self):
        return self.phone
    
    class Meta:
        verbose_name = 'client phone'
        verbose_name_plural = 'client phones'
