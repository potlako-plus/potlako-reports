from django.contrib import admin
from django.urls import path
from .views import HomeView, CancerView, FollowUpView, WorkListView

app_name = 'potlako_reports'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home_url', HomeView.as_view(), name='home_url'),
    path('cancer_url', CancerView.as_view(), name='cancer_url',),
    path('follow_up_url', FollowUpView.as_view(), name='follow_up_url',),
    path('worklist_url', WorkListView.as_view(), name='worklist_url',),
]
