from typing import List
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import (
    AIMessage,
    SystemMessage,
    HumanMessage,
    BaseMessage,
)
import os


class CAMELAgent:

    def __init__(
        self,
        system_message,
        model: AzureChatOpenAI,
        store
    ) -> None:
        self.model = model
        if store == None:
            self.system_message = system_message
            self.init_messages()
            # print("NEW")
        else:
            self.stored_messages = store
            self.system_message = store[0]
            # print("MESSAGES \n",self.stored_messages,"\n SYSTEM MESSAGE \n",self.system_message)

    def reset(self) -> None:
        self.init_messages()
        return self.stored_messages

    def init_messages(self) -> None:
        self.stored_messages = [self.system_message]
        # for msg in self.stored_messages:
            # print("INTIALIZED",msg.content,"\n")

    def update_messages(self, message: BaseMessage) -> List[BaseMessage]:
        self.stored_messages.append(message)
        # for msg in self.stored_messages:
            # print("UPDATED",msg.content,"\n")
        return self.stored_messages
    
    def add_messages(self, messgaes): 
        self.stored_messages = messgaes
        return self.stored_messages

    def step(
        self,
        input_message: HumanMessage,
    ) -> AIMessage:
        messages = self.update_messages(input_message)
        # print("printing the messages here:")
        # print(messages)
        output_message = self.model(messages)
        self.update_messages(output_message)

        return output_message.content

    def store_messages(self):
        return self.stored_messages
    
## Question Sample: "what is your favorite food?", "In which year did you buy your car?", "What is the size of your tshirt?", "From where have you completed your engineering?", "where do you park your car?", "when do you wake up in the morning?"

class AllAgents:

    def __init__(self) -> None:
        self.questions = ["Do you own more than one vehicle?", "Do you always use your turn signals while taking turns?", "Do you drive under the speed limit of 100km/hour?", "Do you talk on the phone while you drive?", "Do you let other people borrow your car?", "Do you have any young drivers in your household?"]
        print(f"The list of questions: {self.questions}")
        self.llm = AzureChatOpenAI(temperature=0.0, 
                            openai_api_key= os.getenv("OPENAI_API_KEY"),
                            openai_api_base=os.getenv("OPENAI_API_BASE"),
                            openai_api_type= os.getenv("OPENAI_API_TYPE"),
                            openai_api_version=os.getenv("OPENAI_API_VERSION"), 
                            deployment_name=os.getenv("DEPLOYMENT_NAME"))
        pass    

    def take_answer_agent(self):

        sys_msg_for_answragent = SystemMessage(content='''You will be taking the insurance survey from user in a conversational tone. You will be thanking the user in case he/she answers your question, and before asking the question, you will give a little brief of what you are trying to do. You will analyze the human answer and then try to find the most closest and accurate answer from the human response. If in case, you could not extract any answer in the human response, you will repeat the question until the user gives the appropriate or closest answer. If the human answer is correct, you will return "I got the answer."

        Your output should be as per the given format                               
        <Format of Output>
        {
          "Thought" : "You will form thought here", 
          "Final response" : "Your final response will come here"                                     
        }
                                               
        ''')

        agent_for_answering = CAMELAgent(sys_msg_for_answragent, self.llm, None)

        human_msg_for_agent = HumanMessage(content='''
        Avoid repeating the question to confirm.
        Instruction: Ask human this -> Are you currently insured? If so, what type of insurance do you have?
        Your response:''')

        agent_for_answering.update_messages(message=human_msg_for_agent)

        AI_msg_for_agent = AIMessage(content='''
        {
            "Thought" : "I have to simply ask the question but have to give a short brief set up to the question that i am going to ask",
            "Final response": "With this question i would like to know about your insurance cover, and past experiences
            
            So can you answer: Are you currently insured? If so, what type of insurance do you have?"
        }''')

        agent_for_answering.update_messages(message=AI_msg_for_agent)

        human_msg_for_agent = HumanMessage(content='''Here is the human response. If the answer is there in human response and if it is correct, you will return "I got the answer."
        Human response: Well last year i bought car insurance
        Your response:''')

        agent_for_answering.update_messages(message=human_msg_for_agent)

        AI_msg_for_agent = AIMessage(content='''{
            "Thought" : "I have to analyse the human answer and try to find the answer to the question. So the human said that he bought car insurance last year, so it means the human is insured with the insurance and type of insurance is 'car insurance'",
            "Final response" : "Okay. So, you are insured and the type of insurance you have is 'Car Insurance'. Thankyou for your answer. I got the answer"
        }''')

        agent_for_answering.update_messages(message=AI_msg_for_agent)

        human_msg_for_agent = HumanMessage(content='''
        Avoid repeating the question to confirm.
        Instruction: Ask human this -> Have you ever filed a claim with your insurance company? If yes, please briefly describe the experience.
        Your response:''')

        agent_for_answering.update_messages(message=human_msg_for_agent)

        AI_msg_for_agent = AIMessage(content='''
        {
            "Thought" : "I have to ask the question again. I have to give a short brief set up to the question that i am going to ask",
            "Final response": "with this question, i would like to know about your past experince with your insurance company.
 
            So can you please answer: Have you ever filed a claim with your insurance company? If yes, please briefly describe the experience. "
        }''')

        agent_for_answering.update_messages(message=AI_msg_for_agent)

        human_msg_for_agent = HumanMessage(content='''Here is the human response. If the answer is there in human response and if it is correct, you will return "I got the answer."
        Human response: I think last year, in november i met with a minor car accident and in that scenrio i went to the insurance company for claim
        Your response:''')

        agent_for_answering.update_messages(message=human_msg_for_agent)

        AI_msg_for_agent = AIMessage(content='''{
            "Thought" : "I have to analyse the human answer and try to find the answer to the question. So the human said that he went to insurance company for minor car accident claim. So, the human has answered that he filed the claim, but yet has not described his experience.",
            "Final response" : "Thankyou for your response. I can see that you filed the claim for minor accident, but it will be great if you could briefly describe the experience as well (if the claim process was smooth or if it was hard)"
        }''')

        agent_for_answering.update_messages(message=AI_msg_for_agent)

        human_msg_for_agent = HumanMessage(content='''Here is the human response. If the answer is there in human response and if it is correct, you will return "I got the answer."
        Human response: The process was mostly smooth 
        Your response:''')

        agent_for_answering.update_messages(message=human_msg_for_agent)

        AI_msg_for_agent = AIMessage(content='''{
            "Thought" : "I have to analyse the human answer and try to find the answer to the question. So the human said that the process was mostly smooth. This means that the user filed the claim and it was mostly smooth with his insurance company for minor car accident",
            "Final response" : "Okay. So, you filed the claim for minor accident and the process of claim was mostly smooth'. Thankyou for your answer. I got the answer, let's move on to the next question now."
        }''')

        agent_for_answering.update_messages(message=AI_msg_for_agent)

        ########## Example 2

        human_msg_for_agent = HumanMessage(content='''
        Avoid repeating the question to confirm. written that it is the first question.
        Instruction: Ask human this -> How important do you consider health insurance to be?
        Your response:''')

        agent_for_answering.update_messages(message=human_msg_for_agent)

        AI_msg_for_agent = AIMessage(content='''
        {
            "Thought" : "I have to simply ask the question but have to give a short brief set up to the question that i am going to ask",
            "Final response": "
            I would like to inquire about your medical insurance-related preferences and experiences.
            
            So can you answer: How important do you consider health insurance to be?"
        }''')

        agent_for_answering.update_messages(message=AI_msg_for_agent)

        human_msg_for_agent = HumanMessage(content='''Here is the human response. If the answer is there in human response and if it is correct, you will return "I got the answer."
        Human response: I think health insurance is important and everyone should have it
        Your response:''')

        agent_for_answering.update_messages(message=human_msg_for_agent)

        AI_msg_for_agent = AIMessage(content='''{
            "Thought" : "I have to analyse the human answer and try to find the answer to the question. So the human said that it is important and everyone should have it. This means that the user finds health insurance important",
            "Final response" : "Yes. In today's time health insurance is really important. Thankyou for your answer. I got the answer, let's move on to the next question now."
        }''')

        agent_for_answering.update_messages(message=AI_msg_for_agent)

        human_msg_for_agent = HumanMessage(content='''
        Avoid repeating the question to confirm.
        Instruction: Ask human this -> Do you currently have health insurance coverage?
        Your response:''')

        agent_for_answering.update_messages(message=human_msg_for_agent)

        AI_msg_for_agent = AIMessage(content='''
        {
            "Thought" : "I have to ask the question again. I have to give a short brief set up to the question that i am going to ask",
            "Final response": "Sine we are talking about health insurance, with this question, i would like to ask you about your current insurance coverage. 
 
            So can you please answer: Do you currently have health insurance coverage?"
        }''')

        agent_for_answering.update_messages(message=AI_msg_for_agent)

        human_msg_for_agent = HumanMessage(content='''Here is the human response. If the answer is there in human response and if it is correct, you will return "I got the answer."
        Human response: I have been associated with insurance provider for last 10 months.
        Your response:''')

        agent_for_answering.update_messages(message=human_msg_for_agent)

        AI_msg_for_agent = AIMessage(content='''{
            "Thought" : "I have to analyse the human answer and try to find the answer to the question. So the human said that he is associated with insurance provider for last 10 months. This means that he bought insurance coverage 10 months back and currently he has health insurance coverage",
            "Final response" : "Thankyou for your answer. I can see that you have health insurance coverage for past 10 months. I got the answer."
        }''')

        agent_for_answering.update_messages(message=AI_msg_for_agent)

        human_msg_for_agent = HumanMessage(content='''
        Avoid repeating the question to confirm.
        Instruction: Ask human this -> What is your preferred option to get information on your health insurance? 
        Your response:''')

        agent_for_answering.update_messages(message=human_msg_for_agent)

        AI_msg_for_agent = AIMessage(content='''
        {
            "Thought" : "I have to ask the question again. I have to give a short brief set up to the question that i am going to ask",
            "Final response": "I would like to know about your preferences to receive the information.
                                     
            So can you please answer: What is your preferred option to get information on your health insurance?"
        }''')

        agent_for_answering.update_messages(message=AI_msg_for_agent)

        human_msg_for_agent = HumanMessage(content='''Here is the human response. If the answer is there in human response and if it is correct, you will return "I got the answer."
        Human response: I think multiple insurance companies are there in the market.
        Your response:''')

        agent_for_answering.update_messages(message=human_msg_for_agent)

        AI_msg_for_agent = AIMessage(content='''{
            "Thought" : "I have to analyse the human answer and try to find the answer to the question. So the human said that there are multiple companies in the market. This talks about competition, but is no where related to the question that was asked about the preference to receive the information.",
            "Final response" : "Thankyou for your response but i could not understand how multiple companies in the market is related to preference to receive the preference to receive the information. Can you please answer my question again?
            here is my question: What is your preferred option to get information on your health insurance? "
        }''')

        agent_for_answering.update_messages(message=AI_msg_for_agent)


        return agent_for_answering