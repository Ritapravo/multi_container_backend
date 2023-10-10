from rest_framework import serializers
from .models import *
import shutil
import tarfile


class DockerComposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DockerCompose
        fields = '__all__'

class MountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mount
        fields = '__all__'
class ConfigFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigFile
        fields = '__all__'

class LabSerialiser(serializers.ModelSerializer):
    
    # files = FileSerializer(many=True, read_only=True)
    dockerCompose = serializers.SerializerMethodField()
    mounts = serializers.SerializerMethodField()
    class Meta:
        model = Lab
        fields = ('id', 'name', 'description', 'dockerCompose', 'created_at', 'mounts')

    def get_dockerCompose(self, obj):
        # Define the logic to compute the value of 'extra_field' here
        data = DockerCompose.objects.get(lab=obj.id)
        serializer=DockerComposeSerializer(data, many=False)
        return serializer.data
    def get_mounts(self, obj):
        data = Mount.objects.filter(lab=obj.id)
        print("==========data=========", data)
        serializer=MountSerializer(data, many=True)
        return serializer.data


class LabUploadSerializer(serializers.Serializer):
    dockerCompose = serializers.ListField(
        child = serializers.FileField(max_length=100000, allow_empty_file = False, use_url = False)
    )
    lab = serializers.CharField(required = True)
    labDescription = serializers.CharField(required = False)
    mounts = serializers.ListField(
        child = serializers.FileField(max_length=100000, allow_empty_file = False, use_url = False)
    )
    configFile = serializers.ListField(
        child = serializers.FileField(max_length=100000, allow_empty_file = False, use_url = False)
    )
    graderMount = serializers.ListField(
        child = serializers.FileField(max_length=100000, allow_empty_file = False, use_url = False)
    )

    def zip_files(self, folder):
        shutil.make_archive(f'public/static/zip/{folder}', 'zip', f'public/static/{folder}')

    def tar(self, folder):
        archive_path = f'public/static/tar_files/{folder}.tar.gz'
        
        # Create the target directory if it doesn't exist
        # os.makedirs(os.path.dirname(archive_path), exist_ok=True)
        with tarfile.open(archive_path, 'w:gz') as archive:
            print("tar ==============================")
            archive.add(f'public/static/{folder}', arcname=str(folder))

    def create(self, validated_data):
        print("validated data============", validated_data)

        temp = validated_data.pop('lab')
        temp2 = validated_data.pop('labDescription')
        lab = Lab.objects.create(name=temp, description=temp2)

        temp = validated_data.pop('dockerCompose')[0]
        dockerCompose = DockerCompose.objects.create(lab = lab, file = temp)

        temp = validated_data.pop('configFile')[0]
        config = ConfigFile.objects.create(lab = lab, file = temp)

        temp = validated_data.pop('graderMount')[0]
        graderMount = GraderMount.objects.create(lab = lab, file = temp)

        mounts = validated_data.pop('mounts')
        mount_objs = []
        for mount in mounts:
            mount_obj = Mount.objects.create(lab = lab, file = mount)
            mount_objs.append(mount_obj)
        self.tar(lab.id)
        print("===================== posted =====================")
        return {'dockerCompose': {}, 'lab': str(lab.id), 'mounts': {}, 'configFile':{}, 'graderMount':{}, 'labDescription': str(lab.description)}