from django.db import models

class Region(models.Model):
    name = models.CharField('Nome', max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Região'
        verbose_name_plural = 'Regiões'

class State(models.Model):
    code = models.CharField('Código UF', max_length=2)
    name = models.CharField('Nome', max_length=150)
    acronym = models.CharField('Sigla', max_length=2)
    region = models.ForeignKey(
        Region,
        verbose_name='Região',
        on_delete=models.CASCADE,
        related_name='states'
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'

class City(models.Model):
    code = models.CharField('Código', max_length=50)
    name = models.CharField('Nome', max_length=150)
    state = models.ForeignKey(
        State,
        verbose_name='Estado',
        on_delete=models.CASCADE,
        related_name='cities'
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Cidade'
        verbose_name_plural = 'Cidades'
