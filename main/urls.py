from django.conf.urls import url

from main.views import AddPic, AddFirstPic

urlpatterns = [

    url(r'^process_data/$', AddPic.as_view(), name="process_data"),
    url(r'^signup/$', AddFirstPic.as_view(), name="signup"),

]