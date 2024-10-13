from cryptography.fernet import Fernet
from flask import Flask, request, jsonify
from pathlib import Path
import json

app = Flask(__name__)

@app.route('/messages', methods=['POST'])
def handle_message_post():
    data = request.form['payload']
    room = request.form['room']
    username = request.form['username']
    password = request.form['password']

    print("========== POST REQUEST FOUND =====================\n")
    print("USERNAME: " + username)
    print("The message sent from client:", data)
    print("ROOM ID:", room)
    print("USERNAME: " + username)
    print("PASSWORD:", password)
    print("\n===============================")
    iswriten = False

    with open('accounts.txt', 'r') as file:
        for line in file:
            if line.startswith(username + ':'):
                key, value = line.split(':', 1)
                print("The user is authenticated!")
                
                room_exists = Path(room + '.txt')
                if room_exists.is_file():
                    print(" Room exists! ")
                    with open(room + '.txt', 'a') as f:
                        f.write("["+ username + "] " + data + '\n')
                        return jsonify({'response': 'OK'})

                else:
                    with open(room + '.txt', 'a') as file:
                        print(" File is now created, writing to file...")
                        file.write("["+ username + "] " + data + '\n')
                        return jsonify({'response': 'new room had to be created.'})

        return jsonify({'message': 'You are not registered!'}), 201

@app.route('/register', methods=['POST'])
def handle_register_post():
    username = request.form['username']
    password = request.form['password']
    admin_key = request.form['admin']
    if admin_key == "dev":
        print("Admin Key is a valid key")
        with open('accounts.txt', 'a') as file:
            print("Account registered!")
            file.write(username + ":" + password + "\n")
        return jsonify({'registered': True}), 200
    else:
        print("Admin key is not a valid key!")
        return jsonify({'auth': False}), 201

    return jsonify({'response': "Admin key was not provided"}), 201

@app.route('/room', methods=['POST'])
def handle_room_post():
    room_id = request.form['room']
    room_exists = Path(room_id + '.txt')

    if room_exists.is_file():
        print("Great, the room exists. Returning the messages.")
        with open(room_id + '.txt', 'r') as file:
            lines = file.readlines()

            combined_text = ''.join([line.strip() for line in lines])
            data = {
                "content": combined_text
            }
            print("returned! no errors. | ROOM: ", room_id)
            return jsonify(data)
    return jsonify({'response': 'room does not exist'}), 201

if __name__ == '__main__':
    app.run(debug=True)
