from django.urls import path
from .views import get_extra_messages, register_user, structured_questions_answers, user_login,add_new_entry,fetch_all_usernames,update_table,empty_the_table,retrieve_table,question,messages,get_llm_response_for_survey_ques,index

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('add_new_entry/', add_new_entry, name='add_new_entry'),
    path('fetch/',fetch_all_usernames,name="fetch"),
    path('update/',update_table,name="update"),
    path('delete/',empty_the_table,name="delete"),
    path('retrieve/',retrieve_table,name="retrieve"),
    path('question/',question,name="question"),
    path('messages/',messages,name="messages"),
    path('fill_survey/', get_llm_response_for_survey_ques, name="Survey Ques"),
    path('extra_messages/', get_extra_messages, name='get_extra_messages'), 
    path('all_ans/',structured_questions_answers,name="answers"), 
    path('upload_file/', index, name='upload_music_file'),

]