
from django.db import models
import uuid
import os

# Create your models here.

class Lab(models.Model):
    # uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=200, blank=False, null=False)
    created_at = models.DateTimeField(auto_now=True)

def get_upload_path(instance, filename):
    return os.path.join(str(instance.lab.id), "docker-compose.yml")

class DockerCompose(models.Model):
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_upload_path)
    created_at = models.DateField(auto_now=True)

def get_upload_path2(instance, filename):
    return os.path.join(str(instance.lab.id) + "/mounts", filename)
class Mount(models.Model):
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_upload_path2)
    created_at = models.DateField(auto_now=True)

def get_upload_path3(instance, filename):
    return os.path.join(str(instance.lab.id) + "/grader", "config.yml")
class ConfigFile(models.Model):
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_upload_path3)
    created_at = models.DateField(auto_now=True)

def get_upload_path4(instance, filename):
    return os.path.join(str(instance.lab.id) + "/grader", "grader.tar.gz")
class GraderMount(models.Model):
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_upload_path4)
    created_at = models.DateField(auto_now=True)