import requests
import json
import time
# Uncomment this if you want to use encryption in the future
# from cryptography.fernet import Fernet

######## LOGIN ############

room = input("What room to connect to? ")
username = input("Enter your username: ")
password = input("Enter your password: ")

####### END OF LOGIN ########

############# REQUEST BELOW ###########

url = 'http://localhost:5000/messages'

def go_request(data):
    response = requests.post(url, data=data)
    print("Your message was sent, your message:", data['payload'])
    print("==== SERVER response ========\n")
    print(response.text)
    print("\n", "================================================================")

def register():
    url = 'http://localhost:5000/register'
    data = {'username': 'helo', 'password': 'hello', 'admin': 'dev'}
    response = requests.post(url, data=data)
    print("==== SERVER response ========\n")
    print(response.text)
    print("\n", "================================================================")

def get_message():
    url = 'http://localhost:5000/messages'
    response = requests.get(url)
    print("==== SERVER response ========\n")
    print(response.text)
    print("\n")
    return response.text

def read_message(room):
    url = 'http://localhost:5000/room'
    data = {'room': room}
    response = requests.post(url, data=data)
    print("==== SERVER response ========\n")
    
    response_data = json.loads(response.text)
    
    content = response_data.get('content', '')
    
    messages = content.split('[')
    
    for message in messages:
        if message.strip():  # Skip empty messages
            print(message.strip())
    
    print("\n", "================================================================")

try:
    for i in range(10000):  
        time.sleep(1)
        print(read_message(room))
        print("\n")
        your_message = input("Enter your message: ")
        
        
        data = {
            'room': room,
            'payload': your_message,
            'username': username,
            'password': password
        }
        go_request(data)

except KeyboardInterrupt:
    print("\nExiting the program.")
