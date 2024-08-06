from rest_framework import status
import langchain
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from demo.source_code.database import retrieve_all_extra_responses, retrieve_all_ques_answers
from .serializers import UserSerializer
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from .models import Message,TranscribedAudio
from django.http import JsonResponse,HttpResponse
from .serializers import MessageSerializer
from langchain.schema import (AIMessage, HumanMessage, SystemMessage)
from demo.source_code.collect_data_qna import GetSurveyAnswersFromUser
import json
from django.views.decorators.csrf import csrf_exempt

from .whisper import transcribe
from .forms import StudentForm
import os
import time
 

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        print(username)
        print(password)

        user = authenticate(username=username, password=password)

        if user is not None: 
            login(request, user)
            return Response({'message': 'Successfully logged in.'}, status=status.HTTP_200_OK)
        
        else: 
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        

@api_view(['POST'])
def add_new_entry(request):
    user_name = request.data.get('username')
    messages = request.data.get('messages')

    existing_message, created = Message.objects.get_or_create(username=user_name)
    print(existing_message)
    print(created)
    existing_message.messages = messages
    existing_message.save()

    return JsonResponse({'message': 'Message added successfully'})


@api_view(['GET'])
def fetch_all_usernames(request):
    usernames = Message.objects.values_list('username', flat=True)
    return JsonResponse({'usernames': list(usernames)})

@api_view(['PUT'])
def update_table(request):
    user_name =  request.data.get('username')
    new_messages = request.data.get('messages')

    try:
        message = Message.objects.get(username=user_name)
        message.messages = new_messages
        message.save()
        return Response({'message': 'Message updated successfully'})
    except Message.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def empty_the_table(request):
    user_name = request.data.get('username')
    try:
        message = Message.objects.get(username=user_name)
        message.delete()
        return Response({'message': 'Table emptied successfully'})
    except Message.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

# @api_view(['GET'])
# def retrieve_table(request, user_name):
#     try:
#         message = Message.objects.get(username=user_name)
#         serialized_message = MessageSerializer(message)
#         return Response(serialized_message.data)
#     except Message.DoesNotExist:
#         return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def retrieve_table(request):
    username = request.data.get('username')
    try:
        # Retrieve the messages for the given username
        messages = Message.objects.get(username=username)
        serializer = MessageSerializer(messages)

        # Deserialize the messages
        deserialized_messages = eval(serializer.data['messages'])

        all_messages = []

        for i, msg_content in enumerate(deserialized_messages):
            i = i + 1
            if i == 1:
                print(msg_content)
                all_messages.append(SystemMessage(content=msg_content))
            elif i % 2 == 0:
                all_messages.append(HumanMessage(content=msg_content))
            else:
                all_messages.append(AIMessage(content=msg_content))

        return JsonResponse(all_messages, safe=False)

    except Message.DoesNotExist:
        return JsonResponse({'message': 'User not found'}, status=404)


@api_view(['POST'])
def question(request):
    if request.method == 'POST':
        username=request.data.get('user_name')
        run = GetSurveyAnswersFromUser(username=username)
        output = run.get_response_for_survey_ques(user_name_val=username)
        
        try:
            final_resp=output.split('''"Final response":''')
            if len(final_resp)==1:
                if(final_resp[0]=='All questions asked'):
                    final_resp=final_resp[0]
                else:
                    final_resp=final_resp[0].split('''{"Thought" :''')[1][:-1]
            else:
                final_resp=final_resp[1][:-1]
        except:
            final_resp=output.split('''"Final response" :''')
            if len(final_resp)==1:
                if(final_resp[0]=='All questions asked'):
                    final_resp=final_resp[0]
                else:
                    final_resp=final_resp[0].split('''{"Thought" :''')[1][:-1]
            else:
                final_resp=final_resp[1][:-1]
            
        return JsonResponse({"status":"success", 
                                "llm_response":f"{final_resp}"})                                                                             
                                                  


@csrf_exempt
@api_view(['POST'])
def get_llm_response_for_survey_ques(request): 
    if request.method == 'POST':
        try:
            human_response=request.data.get('human_text')
            username=request.data.get('username')

                # data = json.loads(request.body.decode('utf-8'))
                # print(f"this is {data}")
                # keys_list = list(data.keys())
                # print(f"these are {keys_list}")

                # if 'human_text' in keys_list and 'username' in keys_list: 
                #     username = data['username']
                #     human_response = data['human_text']
            run = GetSurveyAnswersFromUser(username=username)
            output = run.get_response_for_survey_ques(human_text=human_response, user_name_val=username)
            final_response = ""
            print(f"debugukkkkkk{output}")
            responses = output.split('''}        {''')
            if len(responses) == 1 :
                final_response = output
            else:
                for output in responses:
                    try:
                        final_resp=output.split('''"Final response":''')
                        if len(final_resp)==1:
                            if(final_resp[0]=='All questions asked'):
                                final_resp=final_resp[0]
                            else:
                                final_resp=final_resp[0].split('''{"Thought" :''')[1][:-1]
                        else:
                            final_resp=final_resp[1][:-1]

                    except:
                        final_resp=output.split('''"Final response" :''')
                        if len(final_resp)==1:
                            if(final_resp[0]=='All questions asked'):
                                final_resp=final_resp[0]
                            else:
                                final_resp=final_resp[0].split('''{"Thought" :''')[1][:-1]
                        else:
                            final_resp=final_resp[1][:-1]


                    print(f'debugu{final_resp}')
                    final_response+=final_resp
                    print(f'debuguk{final_response}')
            
            print(f'debugukkk{final_response}')

            return JsonResponse({"status":"success", 
                                    "llm_response":f"{final_response}"})    

            # elif 'human_text' not in keys_list and 'username' in keys_list: 
            #     username = data['username']
            #     run = GetSurveyAnswersFromUser(username=username)
            #     output = run.get_response_for_survey_ques(user_name_val=username)
            #     return JsonResponse({"status":"success", 
            #                          "llm response":f"{output}"})
                            
        #     else: 
        #         return JsonResponse({"status":"failed",
        #                              "error message" : "The payload should contain the username in the specified JSON format with correct key names."})

        except Exception as e: 
            return Response({"message": str(e)}, status=500) 



@api_view(['POST'])
def messages(request):
    if request.method == 'POST':
        messages=request.data.get('message')
        msg=Message(messages=messages)
        msg.save()
        return JsonResponse({'message':'success'})
    


@api_view(['GET']) 
def get_extra_messages(request):
    username = request.query_params.get('username') 
    try:
        extra_messages = retrieve_all_extra_responses(username) 
        if extra_messages: 
            survey_instance = GetSurveyAnswersFromUser(username=username) 
            structured_extra_messages = survey_instance.get_structured_extra_responses(username) 
            return JsonResponse({"status":"success", 
                                "message":structured_extra_messages})   
        else: 
            return Response({"message": "No extra messages found."}, status=404) 
    except Exception as e: 
        return Response({"message": str(e)}, status=500) 


@api_view(['GET']) 
def structured_questions_answers(request): 
    username = request.query_params.get('username') 
    try: 
        survey_instance = GetSurveyAnswersFromUser(username=username) 
        structured_data = survey_instance.get_structured_ques_answers(username) 
       
        return JsonResponse({"status":"success", 
                                "message":structured_data})  
    except Exception as e: 
        return JsonResponse({'message': 'username not provided'}, status=400) 


@api_view(['POST'])
def index(request):
    if request.method == 'POST':

        student_form = StudentForm(request.POST, request.FILES)

        if student_form.is_valid():

            firstname = student_form.cleaned_data['firstname']

            uploaded_file = request.FILES['file']

            

            # Define the local file path where the uploaded file will be saved

            file_path = os.path.join('audio_files/', uploaded_file.name)

            

            # Save the uploaded file to the local directory

            with open(file_path, 'wb') as destination:

                for chunk in uploaded_file.chunks():

                    destination.write(chunk)

 

            # Check if a record with the same 'firstname' already exists

            try:

                transcribed_audio = TranscribedAudio.objects.get(firstname=firstname)

            except TranscribedAudio.DoesNotExist:

                transcribed_audio = TranscribedAudio(firstname=firstname)

 

            # Update the URL to point to the local file path

            transcribed_audio.file = file_path

 

            # Process the uploaded file (assuming you have a transcribe function)

            start_time = time.time()

            text = transcribe(file_path)

            end_time = time.time()

            total_time = end_time - start_time

            print(text)

            print("\n")

            print("Total time taken: {:.2f} seconds".format(total_time))

 

            # Update the transcribed text for the existing record

            transcribed_audio.transcribed_text = text

            transcribed_audio.save()

 

            return JsonResponse({"status": "success", "transcribed_text": text})

        else:

            return JsonResponse({"status": "failed", "error_message": "Form is not valid."}, status=400)