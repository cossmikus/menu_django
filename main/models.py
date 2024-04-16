from django.db import models

class MenuItem(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    url = models.CharField(max_length=200, default='')  # Provide a default value

    def __str__(self):
        return self.name