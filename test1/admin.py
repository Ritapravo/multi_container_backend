from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Lab)
admin.site.register(DockerCompose)
admin.site.register(ConfigFile)
admin.site.register(Mount)
admin.site.register(GraderMount)