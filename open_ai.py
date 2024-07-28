from openai import OpenAI
from dotenv import load_dotenv
import os, time, threading

load_dotenv()
# Open AI API_key and assistant id
OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_assistant_id = os.getenv("openai_assistant_id")
RUN_TEMPERATURE = os.getenv("RUN_TEMPERATURE")

client = OpenAI(api_key=OPEN_AI_API_KEY)

class Assistant:
    
    def __init__(self, client, openai_assistant_id):
        self.client = client
        self.assistant_id = openai_assistant_id
        self.thread_id = None
        self.run_id = None

    def new_thread(self):
        if self.thread_id:
            my_thread = self.client.beta.threads.retrieve(self.thread_id)  # getting thread
            print(f"Current thread: \t\t|{my_thread.id}|\n")
        else:
            empty_thread = self.client.beta.threads.create()
            self.thread_id = empty_thread.id
            print(f"Thread created: \t\t\t|{self.thread_id}|\n")
            return self.thread_id

    def new_message(self, user_message):
        thread_message = self.client.beta.threads.messages.create(
            thread_id=self.thread_id,
            role="user",
            content=user_message
        )
        user_message = thread_message.content[0].text.value
        print(f"Adding a user message into a thread... |{self.thread_id}|")
        return user_message

    def new_run(self):
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread_id,
            assistant_id=self.assistant_id,
            temperature=1
        )
        self.run_id = run.id
        print(f"\nRun Created \t\t- \t|{self.run_id}|")

    def retrieve_run(self):
        while True:
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread_id, 
                run_id=self.run_id,
            )
            print(f"\nAssistant |{self.assistant_id}| processing your request.")

            if run.status == "completed":
                time_calc = run.completed_at - run.created_at
                time_taken = time.strftime("%H:%M:%S", time.gmtime(time_calc))

                print(f"\n_______________RESULTS__________________")
                print(f"Processing completed in: \t{time_taken}")
                print(f"Prompt Tokens used: \t\t{run.usage.prompt_tokens} \nCompletion Tokens used: \t{run.usage.completion_tokens} \nTotal Tokens used: \t\t{run.usage.total_tokens}\n")
                break

            if run.status == "in_progress":
                print("In progress... please wait")
            elif run.status == "canceled":
                print("Your request was canceled for some reason.")
                break
            elif run.status == "failed":
                print("Something went wrong. Please repeat the request.")
                break
            elif run.status == "expired":
                print("Your request has expired.")
                break

            time.sleep(5)

    def list_messages(self):
        messages = self.client.beta.threads.messages.list(
            thread_id=self.thread_id
        )
        last_message = messages.data[0].content[0].text.value

        print("\n<<<CHAT HISTORY>>>\n")
        for message in reversed(messages.data):
            print(f"{message.role}: {message.content[0].text.value:<20}")

        return last_message

    def run_steps(self):
        run_steps = self.client.beta.threads.runs.steps.list(
            thread_id=self.thread_id,
            run_id=self.run_id
        )

        steps = run_steps.data
        print('\n')
        for step in steps:
            print(step)


# Define a function to represent each request task
def request_task(assistant_func, user_message):
    assistant_func.new_thread()  # create a thread
    assistant_func.new_message(user_message)  # add msg to thread
    assistant_func.new_run()  # create a new run
    assistant_func.retrieve_run()  # get the answer 
    reply = assistant_func.list_messages()  # show the thread history

    return reply


# This is the how works logic.
def main() -> None:
    # ----------TEST Open AI API logic----------
    assistant_func = Assistant(client, openai_assistant_id)
    user_messages = ['hello', 'how are you?']
    
    if len(user_messages) > 1:
        # Create threads for each request task
        threads = []
        for message in user_messages:
            thread = threading.Thread(target=request_task, args=(assistant_func, message))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

if __name__ == '__main__':
    main()
