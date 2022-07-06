from django.db import models

# Create your models here.
class review(models.Model):
    prodId = models.CharField(max_length=20)
    userId = models.CharField(max_length=20)
    profName = models.CharField(max_length=50)
    help = models.DecimalField(max_digits=3, decimal_places=2)
    score = models.DecimalField(max_digits=3, decimal_places=2)
    time = models.CharField(max_length=20)
    summary = models.TextField()
    text = models.TextField()

    def __str__(self):
        return f'{self.summary}'


class posting_list(models.Model):
    token = models.CharField(max_length=30, unique=True)
    docs = models.TextField()

    def __str__(self):
        return f'{self.token}'


