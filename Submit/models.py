from django.db import models

# Create your models here.

class NoEmbed(models.Model):
    i_name = models.CharField(max_length=16)
    i_img = models.ImageField(upload_to='embeds/%Y/%m/%d')