from django.db import models
import json
import numpy as np
# Create your models here.

class TextDataset(models.Model):
    text = models.TextField(db_column="text")

    def __str__(self):
        first_30_chars = self.text[:30]

        return f"{first_30_chars}..."


class VectorDataset(models.Model):
    original_pk = models.IntegerField(primary_key=True)
    vector_data = models.TextField()


    def set_vector_data(self,data):
        serialized_data = json.dumps(data.tolist())
        self.vector_data = serialized_data


    def get_vector_data(self):
        serialized_data = json.loads(self.vector_data)
        return np.array(serialized_data)


    def __str__(self):
        return f"PK:{self.pk}, original_pk: {self.original_pk}"