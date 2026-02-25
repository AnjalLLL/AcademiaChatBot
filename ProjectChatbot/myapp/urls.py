from django.contrib import admin
from django.urls import path, include
from myapp.views import chatbot_view

urlpatterns = [
    path("admin/", admin.site.urls),
    #  path("", chatbot_view, name="chat"),
      path("chat/", chatbot_view, name="chatbot") 
]
