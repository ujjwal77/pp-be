from demo.models import llm_messages, ConversationHistory
from langchain.schema import (HumanMessage, AIMessage, SystemMessage)


def fetch_all_usernames():
    # Use the Django ORM to query the llm_messages model for usernames
    usernames = llm_messages.objects.values_list('username', flat=True)
    # print(list(usernames))
    return list(usernames)


def update_table(user_name, new_messages):
    try:
        message = llm_messages.objects.get(username=user_name)
        message.messages = new_messages
        message.save()
        return True
    except llm_messages.DoesNotExist:
        return False
    

def add_new_entry(user_name, messages):
    message_list = str([message.content for message in messages])

    all_users = fetch_all_usernames()

    if user_name not in all_users:
        print("It is a new user")
        # print(user_name)
        # print(all_users)
        new_messages = message_list
        # Create a new llm_messages object and save it to the database
        new_entry = llm_messages(username=user_name, messages=new_messages)
        new_entry.save()
    else:
        print("User already registered before")
        update_table(user_name=user_name, new_messages=message_list)


def retrieve_table(user_name):
    try:
        message_entry = llm_messages.objects.get(username=user_name)
        messages = eval(message_entry.messages)
        
        all_messages = []

        for i, msg_content in enumerate(messages):
            i = i + 1
            if i == 1:
                all_messages.append(SystemMessage(content=msg_content))
            elif i % 2 == 0:
                all_messages.append(HumanMessage(content=msg_content))
            else: 
                all_messages.append(AIMessage(content=msg_content))

        return all_messages

    except llm_messages.DoesNotExist:
        return []
    

def add_new_entry_extra_responses(extra_responses, username_val):
    try:
        # Check if there is an existing entry with extra_responses for the username
        existing_entry = ConversationHistory.objects.filter(username=username_val, extra_responses__isnull=False).exists()

        if existing_entry:
            # Update existing entry
            existing_record = ConversationHistory.objects.get(username=username_val)
            # print(existing_record.extra_responses)
            if len(existing_record.extra_responses)>1:
                existing_extra_responses = eval(existing_record.extra_responses)
                combined_extra_resp = existing_extra_responses + extra_responses
                existing_record.extra_responses = str(combined_extra_resp)
                existing_record.save()
            else: 
                existing_record.extra_responses = str(extra_responses)
                existing_record.save()

        else:
            # Check if there is any entry for the username
            existing_record = ConversationHistory.objects.filter(username=username_val).first()

            if existing_record:
                # Update existing entry
                existing_record.extra_responses = str(extra_responses)
                existing_record.save()
            else:
                # Create a new entry
                new_entry = ConversationHistory(username=username_val, extra_responses=str(extra_responses))
                new_entry.save()

    except Exception as e:
        print(f"An error occurred: {e}")

    return None


def add_new_entry_ques_answers(ques_answers, username_val):
    try:
        # Check if there is an existing entry with messages for the username
        existing_entry = ConversationHistory.objects.filter(username=username_val, messages__isnull=False).exists()

        if existing_entry:
            print("there is an existing extry for username and messages")
            # Update existing entry
            existing_record = ConversationHistory.objects.get(username=username_val)
            print(f"messages got here: {existing_record.messages}")
            if len(existing_record.messages)>1: 
                existing_ques_answers = eval(existing_record.messages)
                combined_ques_answers = {**existing_ques_answers, **ques_answers}
                existing_record.messages = str(combined_ques_answers)
                existing_record.save()
            
            else: 
                existing_record.messages = str(ques_answers)
                existing_record.save()

        else:
            # Check if there is any entry for the username
            existing_record = ConversationHistory.objects.filter(username=username_val).first()

            if existing_record:
                print("there is an existing extry for just username")
                # Update existing entry
                existing_record.messages = str(ques_answers)
                existing_record.save()
            else:
                print("No existing extry")
                # Create a new entry
                new_entry = ConversationHistory(username=username_val, messages=str(ques_answers))
                new_entry.save()

    except Exception as e:
        print(f"An error occurred: {e}")

    return None



def add_new_entry_all_questions(all_questions, username_val):
    try:
        # Check if there is an existing entry with extra_responses for the username
        existing_entry = ConversationHistory.objects.filter(username=username_val, all_questions__isnull=False).exists()

        if existing_entry:
            # Update existing entry
            existing_record = ConversationHistory.objects.get(username=username_val)
            # print(existing_record.all_questions)
            if len(existing_record.all_questions)>1:
                existing_all_questions = eval(existing_record.all_questions)
                combined_extra_ques = existing_all_questions + all_questions
                existing_record.all_questions = str(combined_extra_ques)
                existing_record.save()
            else: 
                existing_record.extra_responses = str(all_questions)
                existing_record.save()

        else:
            # Check if there is any entry for the username
            existing_record = ConversationHistory.objects.filter(username=username_val).first()

            if existing_record:
                # Update existing entry
                existing_record.extra_responses = str(all_questions)
                existing_record.save()
            else:
                # Create a new entry
                new_entry = ConversationHistory(username=username_val, all_questions=str(all_questions))
                new_entry.save()

    except Exception as e:
        print(f"An error occurred: {e}")

    return None



def retrieve_all_questions(username_val):
    
    existing_record = ConversationHistory.objects.get(username=username_val)

    if len(existing_record.all_questions)>1:

        existing_all_questions = eval(existing_record.all_questions)

        
        return existing_all_questions
    
    else: 
        return []
    

def retrieve_all_extra_responses(username_val): 
    existing_record = ConversationHistory.objects.get(username=username_val) 
    if len(existing_record.extra_responses)>1: 
        existing_all_extra_responses = eval(existing_record.extra_responses) 
        return existing_all_extra_responses 
    else: 
        return [] 

def retrieve_all_ques_answers(username_val): 
    existing_record = ConversationHistory.objects.get(username=username_val) 
    if len(existing_record.messages)>1: 
        existing_ques_answers = eval(existing_record.messages) 
        return existing_ques_answers 
    else: 
        return [] 








