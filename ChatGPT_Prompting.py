from openai import OpenAI
client = OpenAI()

startPrompt = ""

allMessages = [{"role": "system", "content": startPrompt}]     #Initializing structure for a context window for ChatGPT, which is consisting of messages.


def User_PromptChatGPT_ReturnResponse(_userChatList, _promptMessage, _messageRole):
    
    _userChatList.append({"role": _messageRole, "content": _promptMessage})      #Appends the current prompt message to the chat list input as an argument in the function's parameters. This is meant to be the chat list of what a specific has said and ChatGPT's responses to it.
    allMessages.append({"role": _messageRole, "content": _promptMessage})      #Append the message  to the global ChatGPT messages list, which is the chat list of everything that has been said by everyone (all users AND ChatGPT)
    
    chatCompletion = client.chat.completions.create(
        model= "gpt-3.5-turbo", #gpt-4o-mini, gpt-3.5-turbo
        messages= _userChatList
    )
    
    _chatGPT_response = chatCompletion.choices[0].message.content
    _userChatList.append({"role": "assistant", "content": _chatGPT_response})
    allMessages.append({"role": "assistant", "content": _chatGPT_response})      #Appends what
    
    return _chatGPT_response



def Simple_PromptChatGPT_ReturnResponse(_promptMessage, _messageRole):
    
    allMessages.append({"role": _messageRole, "content": _promptMessage})      #Append the message  to the global ChatGPT messages list, which is the chat list of everything that has been said by everyone (all users AND ChatGPT)

    chatCompletion = client.chat.completions.create(
        model= "gpt-3.5-turbo", #gpt-4o-mini, gpt-3.5-turbo
        messages= allMessages
    )

    _chatGPT_response = chatCompletion.choices[0].message.content
    allMessages.append({"role": "assistant", "content": _chatGPT_response})    # Append ChatGPT's response to the messages chat list

    return _chatGPT_response


def Add_System_Prompt_ChatGPT(_promptMessage):
    allMessages.append({"role": "system", "content": _promptMessage})

def Add_User_Prompt_ChatGPT(_promptMessage):
    allMessages.append({"role": "system", "content": _promptMessage})