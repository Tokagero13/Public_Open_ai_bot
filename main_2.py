import  os, json, aiohttp, asyncio
from dotenv import load_dotenv
from typing import Final
from open_ai import *

load_dotenv()
# Telegram Token and botname
bot_token = os.getenv("TELEGRAM_TOKEN")
bot_username: Final = os.getenv('TELEGRAM_BOT_USERNAME')

# Call the class from open_ai
assistant_func = Assistant(client, openai_assistant_id)

# Function to collect messages from Telegram and put them into the queue
async def listener(request_list):
    last_update_id = None 

    async with aiohttp.ClientSession() as session:
        while True:
            print("Waiting for message...")
            await asyncio.sleep(1)
            url = "https://api.telegram.org/bot{}/getUpdates".format(bot_token)
            params = {'offset': last_update_id} if last_update_id else {}
            async with session.get(url, params=params) as response:
                updates = await response.json()

                if 'result' in updates and updates['result']:
                    for update in updates['result']:
                        last_update_id = update['update_id'] + 1
                        input = {
                            "user_message": update
                            }
                        print(f"\nGET USER MESSAGE INPUT: {json.dumps(input, indent=4)}")
                        request_list.append(input)
                        print("Collected in the |request_list|")
                        await asyncio.sleep(1)  # Simulate delay in collecting messages
                else:
                    print("No new updates.")

async def test_reply(chat_id, user_message) -> dict: #AI generatin ai_message
    print("Following text ---> '{}' is processing by AI bot".format(user_message))
    print(f"\nRetrieving reply from AI for |{chat_id}| in...")
    for i in range(4, 0, -1): #Simultaing AI reply generation
        print(f"Chat ({chat_id}) reply ready in {i}...")
        await asyncio.sleep(1)
    response = "Hello {}, I am an AI bot. How can I help you?".format(chat_id)
    output = {              
                "ai_message": {
                    "reply": response,
                    "chat_id": chat_id
                }
            }
    return output

async def reply(user_message, chat_id):
    asyncio.sleep(0.5)
    assistant_func.new_thread() #create a thread
    assistant_func.new_message(user_message) #add msg to thread
    assistant_func.new_run() #create a new run
    assistant_func.retrieve_run() #get the answer 
    response = assistant_func.list_messages() #show the thread history

    output = {
            "ai_message": {
                "reply": response,
                "chat_id": chat_id
            }
        }
    return output

# Function to consume messages from the queue and process them
async def consumer(request_list, response_list):
    async with aiohttp.ClientSession() as session:
        while True:
            if not request_list:
                await asyncio.sleep(1)
                print("\nResponse Queue is empty")
            else:
                extracted_input = request_list.pop(0) #extract message
                print("\nProcessing |INPUT| message...")

                data = extracted_input["user_message"]
                message = data["message"] # Extract message key-value pair

                user_message = message["text"] # Extract user message
                print("User Message: {}".format(user_message))
                chat_id = data['message']['chat']['id']  # Update this to extract chat_id from msg

                print("Following text ---> '{}' is processing by AI bot".format(user_message))
                print(f"\nRetrieving reply from AI for |{chat_id}| in...")

                response = await reply(user_message, chat_id)

                # response = await test_reply(chat_id, user_message)
                
                response_list.append(response)

                print(response_list)

                if user_message == "END":
                    break


# Function to send a Telegram message
async def sender(response_list):
    async with aiohttp.ClientSession() as session:
        while True:                
            await asyncio.sleep(0.5)
            if not response_list:
                await asyncio.sleep(1)
                print("\nResponse Queue is empty")
            else:
                extracted_output = response_list.pop(0)

                print("\nThe |queue| has message!")
                print(f"send_telegram_message: {extracted_output}")

                # Extract the inner dictionary
                
                reply = extracted_output['ai_message']['reply']
                chat_id = extracted_output['ai_message']['chat_id']
                print(f"Chat ID: {chat_id} has a reply: {reply}")

                # Send the reply to Telegram
                url = "https://api.telegram.org/bot{}/sendMessage".format(bot_token)
                payload = {
                    'chat_id': chat_id,
                    'text': reply
                }

                async with session.post(url, data=payload) as response:
                    response_json = await response.json()
                    print(response_json)


async def main():
    request_list = []
    response_list = []

    listener_task = asyncio.create_task(listener(request_list))
    sender_task = asyncio.create_task(sender(response_list))
    task = asyncio.create_task(consumer(request_list, response_list))

    await listener_task
    await task
    await sender_task

# Run the main function
if __name__ == '__main__':
    asyncio.run(main())