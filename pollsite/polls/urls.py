from django.urls import path
from . import apiviews
from . import views
app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('questions/', apiviews.QuestionsView.as_view(), name='questions_view'),
    path('questions/<int:question_id>/', apiviews.QuestionDetailView.as_view(), name='question_detail_view'),
    path('questions/<int:question_id>/choices/', apiviews.choices_view, name='choices_view'),
    path('questions/<int:question_id>/vote/', apiviews.vote_view, name='vote_view'),
    path('questions/mailto/', apiviews.TaskView.as_view(), name='task_view'),
    path('questions/<int:question_id>/result/', apiviews.QuestionResultView.as_view(), name='question_result_view')
]