from django.db import models
from django.db.models.deletion import CASCADE
from django.core.validators import int_list_validator


class Patent(models.Model):
    patent_id = models.CharField(max_length=128)


class Sequence(models.Model):
    seq_id = models.CharField(max_length=10)
    sequence = models.CharField(max_length=5000)
    patent = models.ForeignKey(Patent, 
                                on_delete=CASCADE, related_name="sequences")


class Epitope(models.Model):
    epitope = models.CharField(validators=[int_list_validator], 
                                max_length=512)
    patent = models.ForeignKey(Patent, 
                                on_delete=CASCADE, related_name="epitopes")