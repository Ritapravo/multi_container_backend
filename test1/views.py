from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from django.http import Http404
import os
import requests
import tarfile
import subprocess
import shutil
# Create your views here.

def home(request):
    return HttpResponse("Hello")

class getlabs(APIView):
    def get_object(self, pk):
        try:
            return Lab.objects.get(id=pk)
        except Lab.DoesNotExist:
            return Response({"Not found"})
    def get(self,request, pk=None):
        if(pk is None):
            data = Lab.objects.all()
            serializer=LabSerialiser(data, many=True)
            return Response(serializer.data, status=200)
        else:
            print(pk)
            data = self.get_object(pk)
            serializer=LabSerialiser(data)
            return Response(serializer.data, status=200)

class createLab(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = LabUploadSerializer(data = data)

            if(serializer.is_valid()):
                serializer.save()
                return Response({
                    'status':200,
                    'message' : 'files uploaded successfully',
                    'data' : serializer.data
                })
            return Response({
                'status':400, 
                'message': 'something went wrong',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error":e})
        


# ============ Student Part ===============


def start_containers(id, lab_path):
    print("lab_path ==== ", lab_path)
    start_script_location = "/home/ritpravo/Desktop/MTP/build/start.sh"
    stop_script_location = "/home/ritpravo/Desktop/MTP/build/stop.sh"
    subprocess.run(["cp", start_script_location, lab_path+'/'], stdout=subprocess.PIPE, text=True)
    subprocess.run(["cp", stop_script_location, lab_path+'/'], stdout=subprocess.PIPE, text=True)
    result1 = subprocess.run(["bash", lab_path+'/start.sh', lab_path+'/docker-compose.yml' ], stdout=subprocess.PIPE, text=True)
    print (result1)

def download_and_extract_tar(id, download_url, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    tar_filename = f'{id}.tar.gz'
    tar_filepath = os.path.join(output_dir, tar_filename)

    directory_path = os.path.join(output_dir, str(id))
    if(os.path.exists(directory_path)):
        print("Already downloaded")
    else:
        try:
            # Download the tar.gz file
            response = requests.get(download_url)
            response.raise_for_status()  # Check for any download errors

            # Save the downloaded file
            with open(tar_filepath, 'wb') as tar_file:
                tar_file.write(response.content)
                tar_file.close()

            print("========== reached ==========", tar_filepath)
            # Extract the tar.gz file
            # with tarfile.open(tar_filepath, 'r:gz') as archive:
            #     archive.extractall(path=output_dir)
            result = subprocess.run(["tar", "-xvf", tar_filepath, "-C", output_dir], stdout=subprocess.PIPE, text=True)
            print(result.stdout)
            temp = output_dir+str(id)+'/grader/'
            result = subprocess.run(["tar", "-xvf", temp+'grader.tar.gz', "-C", temp], stdout=subprocess.PIPE, text=True)
            print(["mv", temp+'grader/*', temp])
            result = subprocess.run(f'mv {temp}grader/* {temp}', shell=True)
            result = subprocess.run(["rmdir" , temp+'grader/'], stdout=subprocess.PIPE, text=True)
            # mv ./grader/* ./ && rmdir grader
            for filename in os.listdir(output_dir+str(id)+'/mounts/'):
                temp = output_dir+str(id)+'/mounts/'
                if filename.endswith('.tar.gz'):
                    result = subprocess.run(["tar", "-xvf", temp+filename, "-C", temp], stdout=subprocess.PIPE, text=True)

            print(f"Downloaded and extracted '{tar_filepath}' to '{output_dir}'")
        except requests.exceptions.RequestException as e:
            print(f"Error: Failed to download file - {e}")
        except tarfile.TarError as e:
            print(f"Error: Failed to extract file - {e}")
    start_containers(id, directory_path)

class attemptLab(APIView):
    def get_object(self, pk):
        try:
            return Lab.objects.get(id=pk)
        except Lab.DoesNotExist:
            return Response({"Not found"})
    def get(self,request, pk=None):
        print(pk)
        data = self.get_object(pk)
        id = pk  
        download_url = f"http://0.0.0.0:8000/media/tar_files/{id}.tar.gz"
        output_dir = os.path.expanduser('~/Documents/mlab/')

        download_and_extract_tar(id, download_url, output_dir)
        return Response({"successful"})
    

class exitLab(APIView):
    def get_object(self, pk):
        try:
            return Lab.objects.get(id=pk)
        except Lab.DoesNotExist:
            return Response({"Not found"})
    def get(self,request, pk=None):
        try:
            id = pk
            base_dir = os.path.expanduser('~/Documents/mlab/')
            lab_path = os.path.join(base_dir, str(id))
            stop_script_location = "/home/ritpravo/Desktop/MTP/build/stop.sh"
            subprocess.run(["cp", stop_script_location, lab_path+'/'], stdout=subprocess.PIPE, text=True)
            result1 = subprocess.run(["bash", lab_path+'/stop.sh', lab_path+'/docker-compose.yml' ], stdout=subprocess.PIPE, text=True)
            print (result1)
            subprocess.run(["docker", 'stop', 'grader' ], stdout=subprocess.PIPE, text=True)
            print("exit")
            return Response({"successful"})
        except Exception as e:
            return Response({"Error"})
            print(e)

# evaluateLab  
class evaluateLab(APIView):
    def get_object(self, pk):
        try:
            return Lab.objects.get(id=pk)
        except Lab.DoesNotExist:
            return Response({"Not found"})
    def get(self,request, pk=None):
        try:
            id = pk
            base_dir = os.path.expanduser('~/Documents/mlab/')
            lab_path = os.path.join(base_dir, str(id))
            graderMount = os.path.join(lab_path, 'grader')
            # docker run --rm --name grader -v ./grader:/grader -v  /var/run/docker.sock:/var/run/docker.sock grader_image
            res = subprocess.run(["docker", "run", "--rm", "--name", "grader", "-v", str(graderMount)+ ":/grader","-v", "/var/run/docker.sock:/var/run/docker.sock", "grader_image"], stdout=subprocess.PIPE,stderr=subprocess.PIPE, text=True)
            print (res)
            return Response({"result" :res.stdout, "error":res.stderr})
        except Exception as e:
            return Response({"Error"})
            print(e)
