
from django.db import models
import uuid
import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import shutil

# Create your models here.

class Lab(models.Model):
    # uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=200, blank=False, null=False)
    description = models.CharField(max_length=20000, default='', blank=True, null=False)
    created_at = models.DateTimeField(auto_now=True)
@receiver(pre_delete, sender=Lab)
def mymodel_delete(sender, instance, **kwargs):
    # Delete the associated file when the MyModel instance is deleted
    if instance.name:
        directory_path  = os.path.join("public/static/", str(instance.id))
        tar_path = os.path.join("public/static/tar_files/"+ str(instance.id)+'.tar.gz')
        try:
            if os.path.exists(tar_path):
                os.remove(tar_path)
            shutil.rmtree(directory_path)
        except Exception as e:
            print(f"Error deleting directory: {e}")

def get_upload_path(instance, filename):
    print("path==",os.path.join(str(instance.lab.id), "docker-compose.yml"))
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