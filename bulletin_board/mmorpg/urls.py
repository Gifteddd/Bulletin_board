from django.urls import path
from .views import *

urlpatterns = [
    path('mmorpg/', MmorpgPage.as_view(), name='mmorpg'),
    path('advert/create/', AdvertCreate.as_view(), name='advert_create'),
    path('advert/<int:pk>/', AdvertDetail.as_view(), name='ad_detail'),
    path('advert/<int:pk>/update/', AdvertUpdate.as_view(), name='advert_update'),
    path('advert/<int:pk>/delete/', AdvertDelete.as_view(), name='advert_delete'),
    path('comments', Comments.as_view(), name='comments'),
    path('comments/<int:pk>', Comments.as_view(), name='comments'),
    path('commentt/<int:pk>', Commentt.as_view(), name='commentt'),
    path('response/accept/<int:pk>', response_accept),
    path('response/delete/<int:pk>', response_delete),
    path('', lambda request: redirect('mmorpg/', permanent=False)),
    ]
