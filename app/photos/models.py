from django.db import models


class Photo(models.Model):
    dest_file_path = models.CharField(max_length=255, unique=True)
    hash_md5 = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return f"Student {self.dest_file_path} ({self.hash_md5})"
