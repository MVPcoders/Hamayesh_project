# from django.urls import path
# from .views import aricle
#
# urlpatterns = [
#     path('new-article/', aricle, name='new_article'),
# ]
# from .views import submit_article
# urlpatterns = [
#     path('new-article/', submit_article, name='new_article'),
# ]

from django.urls import path
from . import views
from .views import  SubmitArticle, GenerateCertificate, VerifyArticle

urlpatterns = [
    path('new-article/', SubmitArticle.as_view(), name='new_article'),
    path('edit-article/', views.UserArticleEdit.as_view(), name='edit_article'),
    path('delete-article/', views.user_delete_article, name='delete_article'),
    path('correct-article/', views.send_correction_request, name='correct_article'),
    path('article-cer-maker/',GenerateCertificate.as_view(), name='generate_certificate'),
    path('save-certificate/', views.save_certificate, name='save_certificate'),
    path("article/verify/<str:code>/", VerifyArticle.as_view(), name="article_verify")

]



