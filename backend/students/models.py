from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=140)
    course = models.CharField(max_length=140)
    rating = models.PositiveIntegerField()

    class Meta:
        ordering = ['name',]
    
    def __str__(self):
        return '-'.join((self.name, self.course))


