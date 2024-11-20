from openai import OpenAI
client = OpenAI()

startPrompt = ""

messages = [{"role": "system", "content": startPrompt}]     #Initializing structure for a context window for ChatGPT, which is consisting of messages.


def User_PromptChatGPT_ReturnResponse(_userChatList, _promptMessage, _messageRole):
    
    _userChatList.append({"role": _messageRole, "content": _promptMessage})      #Appends the current prompt message to the chat list input as an argument in the function's parameters. This is meant to be the chat list of what a specific has said and ChatGPT's responses to it.
    #messages.append({"role": _messageRole, "content": _promptMessage})      #Append the message  to the global ChatGPT messages list, which is the chat list of everything that has been said by everyone (all users AND ChatGPT)
    
    chatCompletion = client.chat.completions.create(
        model= "gpt-4o-mini",
        messages= _userChatList
    )

    _chatGPT_response = chatCompletion.choices[0].message
    _userChatList.append({"role": "assistant", "content": _chatGPT_response})
    messages.append({"role": "assistant", "content": _chatGPT_response})      #Appends what
    
    return _chatGPT_response



def Simple_PromptChatGPT_ReturnResponse(_promptMessage, _messageRole):

    messages.append({"role": _messageRole, "content": _promptMessage})      #Append the message  to the global ChatGPT messages list, which is the chat list of everything that has been said by everyone (all users AND ChatGPT)

    chatCompletion = client.chat.completions.create(
        model= "gpt-4o-mini",
        messages= messages
    )

    _chatGPT_response = chatCompletion.choices[0].message
    messages.append({"role": "assistant", "content": _chatGPT_response})

    return _chatGPT_response