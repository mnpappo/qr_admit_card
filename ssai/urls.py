from django.urls import path

from . import views
from .views import StudentInfoListView

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:student_id>', views.qr_to_admit_page, name='qr_to_admit_page'),
    path('students', StudentInfoListView.as_view()),
]