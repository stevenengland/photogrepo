from django.db import models


class Photo(models.Model):
    dest_file_path = models.CharField(max_length=255, unique=True)
    hash_md5 = models.CharField(max_length=32, unique=True)
    hash_perceptual = models.CharField(max_length=32)
    hash_difference = models.CharField(max_length=32)
    hash_average = models.CharField(max_length=32)
    hash_wavelet = models.CharField(max_length=32)
    encoding_cnn = models.TextField()

    def __str__(self):
        return f"Photo {self.dest_file_path} ({self.hash_md5})"
