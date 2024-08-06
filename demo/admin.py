from django.contrib import admin
from .models import Message,CustomUser,llm_messages,ConversationHistory,TranscribedAudio
# Register your models here.
admin.site.register(Message)
admin.site.register(CustomUser)
admin.site.register(llm_messages)
admin.site.register(ConversationHistory)
admin.site.register(TranscribedAudio)