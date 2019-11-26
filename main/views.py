import os

from django.http import JsonResponse
from django.utils.crypto import get_random_string
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from process.main import process, process1


class AddFirstPic(generics.CreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [AllowAny]

    def post(self, request, **kwargs):
        up_file = request.FILES['file']
        name = request.POST['user']

        if not os.path.exists('static/pictures/'):
            os.makedirs('static/pictures/')

        unique_id = get_random_string(length=12)
        ext = ".jpg"
        img_path = 'static/pictures/' + name

        destination = open(img_path + ext, 'wb+')
        for chunk in up_file.chunks():
            destination.write(chunk)
            destination.close()

        process1(img_path+ext, name)

        delete()

        return JsonResponse({"path": img_path, "name": name})


class AddPic(generics.CreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [AllowAny]

    def post(self, request, **kwargs):
        up_file = request.FILES['file']
        up_name = request.POST['user']

        if not os.path.exists('static/pictures/'):
            os.makedirs('static/pictures/')

        unique_id = get_random_string(length=12)
        ext = ".jpg"
        img_path = 'static/pictures/' + unique_id

        destination = open(img_path + ext, 'wb+')
        for chunk in up_file.chunks():
            destination.write(chunk)
            destination.close()

        # Return processed data as JSON.
        found_data = process_image(img_path + ext, up_name)
        if found_data is not None:
            return JsonResponse(found_data)
        else:
            return Response("Nothing")


# This function is responsible for modifying the image properties the right way and optimize it for data extraction.
# It can be re-called a second time if no data was found analyzing the regular image.
def process_image(path, name):
    acc = process(path, "static/pictures/" + name + ".jpg")

    delete()
    # Parse the found results.
    found_data = {'result': "%.2f" % acc, 'name': name}

    return found_data


def delete():
    folder1 = "static/pictures/output/correlation"
    folder2 = "static/pictures/output/unsharpening"
    folder3 = "static/pictures/output/final"
    folder4 = "static/pictures/output/extracted_signatures"
    for the_file in os.listdir(folder1):
        file_path = os.path.join(folder1, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

    for the_file in os.listdir(folder2):
        file_path = os.path.join(folder2, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

    for the_file in os.listdir(folder3):
        file_path = os.path.join(folder3, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)
    for the_file in os.listdir(folder4):
        file_path = os.path.join(folder4, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)
