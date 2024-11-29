import json
import sys
import random
import time
import os
from datetime import datetime
from http.client import HTTPSConnection

def get_timestamp():
    """
    Returns a timestamp in the format YYYY-MM-DD HH:MM:SS
    """
    return "[" + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "]"

def random_sleep(duration, min_random, max_random):
    sleep_duration = duration + random.randint(min_random, max_random)
    print(f"{get_timestamp()} Sleeping for {sleep_duration} seconds")
    time.sleep(sleep_duration)

def read_info():
    try:
        user_id = os.getenv("USER_ID")
        token = os.getenv("DISCORD_TOKEN")
        channel_url = os.getenv("CHANNEL_URL")
        channel_id = os.getenv("CHANNEL_ID")
        delay = os.getenv("DELAY_BETWEEN_MESSAGES")
        sleep = os.getenv("SLEEP_TIME")
        if not all([user_id, token, channel_url, channel_id, delay, sleep]):
            raise ValueError("One or more environment variables are missing")
        return [user_id, token, channel_url, channel_id, delay, sleep]
    except Exception as e:
        print(f"{get_timestamp()} Error reading environment variables: {e}")
        return None

def configure_info():
    try:
        user_id = input("User-ID: ")
        token = input("Discord token: ")
        channel_url = input("Discord channel URL: ")
        channel_id = input("Discord channel ID: ")
        delay = input("Delay (in seconds) between messages: ")
        sleep = input("Sleep time (in seconds): ")
        os.environ["USER_ID"] = user_id
        os.environ["DISCORD_TOKEN"] = token
        os.environ["CHANNEL_URL"] = channel_url
        os.environ["CHANNEL_ID"] = channel_id
        os.environ["DELAY_BETWEEN_MESSAGES"] = delay
        os.environ["SLEEP_TIME"] = sleep
        print(f"Environment variables set, please rerun to start!")
    except Exception as e:
        print(f"{get_timestamp()} Error configuring user information: {e}")
        exit()

def set_channel():
    info = read_info()
    if info:
        user_id, token, _, _, delay, sleep = info
        channel_url = input("Discord channel URL: ")
        channel_id = input("Discord channel ID: ")
        os.environ["CHANNEL_URL"] = channel_url
        os.environ["CHANNEL_ID"] = channel_id
        print(f"Environment variables set, please rerun to start!")

def show_help():
    print("Showing help for discord-auto-messenger")
    print("Usage:")
    print("  'python3 auto.py'               :  Runs the automessenger. Type in the wait time and take a back seat.")
    print("  'python3 auto.py --config'      :  Configure settings.")
    print("  'python3 auto.py --setC'  :  Set channel to send message to. Including Channel ID and Channel URL")
    print("  'python3 auto.py --help'        :  Show help")

def send_message(conn, channel_id, message_data, header_data):
    try:
        conn.request("POST", f"/api/v6/channels/{channel_id}/messages", message_data, header_data)
        resp = conn.getresponse()
        if 199 < resp.status < 300:
            print(f"{get_timestamp()} Message {message_data} sent!")
    except Exception as e:
        print(f"{get_timestamp()} Error sending message: {e} | {message_data}")

def get_connection():
    return HTTPSConnection("discordapp.com", 443)

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--config" and input("Configure? (y/n)") == "y":
            configure_info()
            return
        elif sys.argv[1] == "--setC" and input("Set channel? (y/n)") == "y":
            set_channel()
            return
        elif sys.argv[1] == "--help":
            show_help()
            return

    info = read_info()
    if not info or len(info) != 6:
        print(
            f"{get_timestamp()} An error was found inside the environment variables. Please ensure the following "
            f"environment variables are set: USER_ID, DISCORD_TOKEN, CHANNEL_URL, CHANNEL_ID, DELAY_BETWEEN_MESSAGES, "
            f"and SLEEP_TIME. Try again with python3 auto.py"
        )
        configure_info()
        return

    header_data = {
        "content-type": "application/json",
        "user-id": info[0],
        "authorization": info[1],
        "host": "discordapp.com",
        "referrer": info[2]
    }

    print(f"{get_timestamp()} Messages will be sent to " + header_data["referrer"] + ".")

    delay_between_messages = int(info[4])
    sleep_time = int(info[5])

    while True:
        try:
            with open("messages.txt", "r") as file:
                messages = file.read().splitlines()
        except FileNotFoundError:
            print(f"{get_timestamp()} Messages file not found.")
            return

        for message in messages:
            message_data = json.dumps({"content": message})
            conn = get_connection()
            send_message(conn, info[3], message_data, header_data)
            conn.close()
            random_sleep(delay_between_messages, 1, 10)

        print(f"{get_timestamp()} Finished sending all messages!")
        random_sleep(sleep_time, 20, 150)

if __name__ == "__main__":
    main()