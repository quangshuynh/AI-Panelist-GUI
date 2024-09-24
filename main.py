"""
Ollama A.I. Panelist GUI App
09/23/24
Quang Huynh
"""

import tkinter as tk
from tkinter import scrolledtext, simpledialog
import ollama as o
import random

dolphin = "dolphin-llama3"

class Agent:
    def __init__(self, name, description, model=dolphin):
        self.name = name
        self.description = description
        self.model = model
        self.history = [{'role': 'system', 'content': f"You are {name}, {description}."}]

    def add_message(self, message, role='assistant'):
        self.history.append({'role': role, 'content': message})

    def response(self, message):
        self.history.append({'role': 'user', 'content': message})
        response = o.chat(
            model=self.model,
            messages=self.history
        )
        self.history.append({'role': 'assistant', 'content': response['message']['content']})
        return response

    def get_output(self, message):
        response = o.chat(
            model=self.model,
            messages=self.history + [{'role': 'user', 'content': message}]
        )
        return response


class AIPanelGame:
    def __init__(self, root, agents, username):
        """
        A class representing the AI Panel Game GUI.
        This class handles the main functionality of the game, including accepting user input,
        displaying responses from AI panelists, and managing the chat history.

        :param root: The root window of the Tkinter application
        """
        self.agents = agents
        self.root = root
        self.root.title("AI Panel Game")
        self.username = username

        # Instructions label
        self.instructions = tk.Label(root, text="Ask a question to the AI panelists")
        self.instructions.pack(pady=5)

        # User input box
        self.prompt_entry = tk.Entry(root, width=100)
        self.prompt_entry.pack(pady=10)

        # Submit button
        self.submit_button = tk.Button(root, text="Submit", command=self.ask_question)
        self.submit_button.pack(pady=5)

        # Scrolled text box for chat history
        self.chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=50)
        self.chat_history.pack(pady=10)
        self.chat_history.config(state=tk.DISABLED)  # Disable typing in the chat history
        self.chat_history.tag_configure("bold", font=("Comic Sans", 12, "bold"))
        self.chat_history.tag_configure("normal", font=("Comic Sans", 12))

        # Clear button
        self.clear_button = tk.Button(root, text="Clear", command=self.clear_chat)
        self.clear_button.pack(pady=5)

        # Available names
        self.available_names = [
            'Quang', 'Catherine', 'Charlie', 'David', 'Kai', 'Frank', 'Abby', 'Hannah', 'Olivier', 'Jack', 'Karen', 'Leo',
            'Mia','Nathan', 'Olivia', 'Paul', 'Quinn', 'Rachel', 'Sam', 'Tina', 'Bob', 'Vince', 'Wendy', 'Xander',
            'Vivian', 'Zane', 'Aaron', 'Bianca', 'Caleb', 'Diana', 'Edward', 'Fiona', 'George', 'Harper', 'Isaac',
            'Julia', 'Kevin', 'Liam', 'Maya', 'Nina', 'Omar', 'Penny', 'Quincy', 'Rose', 'Sean', 'Tara', 'Ulysses',
            'Victor', 'Willow', 'Uday', 'Michael', 'Zachary', 'Amber', 'Brian', 'Clara','Derek', 'Ella', 'Felix',
            'Gabriel', 'Hazel', 'Ian', 'Jade', 'Kyle', 'Lara', 'Max', 'Nora', 'Oscar', 'Parker', 'Quentin', 'Rebecca',
            'Sophie', 'Tom', 'Edward', 'Vivian', 'Walter', 'Xavier', 'Yvonne', 'Zoey', 'Anthony', 'Bella', 'Chris',
            'Daphne', 'Elliot', 'Freya', 'Gavin', 'Hope', 'John', 'Jasper', 'Kira', 'Lucas', 'Mason', 'Nolan',
            'Ophelia', 'Preston', 'Ruby', 'Spencer', 'Tessa', 'Uriel', 'Violet', 'Wesley', 'Evan', 'CJ', 'Tate',
            'Trevor'
        ]
        self.used_names = []

    def randomize_unique_names(self):
        """
        A function to select a unique name from the available names

        This method ensures that no two names are the same by removing the chosen name from list of available names
        :return: A unique name
        """
        if len(self.available_names) == 0:
            # reset the list if all names have been used
            self.available_names = self.used_names
            self.used_names = []
        name = random.choice(self.available_names)
        self.available_names.remove(name)
        self.used_names.append(name)
        return name

    def ask_question(self):
        """
        A function to handle user input and display AI responses.

        This method gets the user's question, sends it to multiple AI panelists,
        and updates the chat history with the responses.

        :return: None
        """
        agent_list = self.agents
        user_question = self.prompt_entry.get()
        if user_question.strip() == "":
            return  # Don't process empty questions

        # Display the user's question in the chat
        self.update_chat((f"{self.username} (Moderator) ", user_question))

        # Get AI responses from panelists
        user_question = (self.username, user_question)
        for agent in agent_list:
            agent.add_message(f"{user_question[0]}: {user_question[1]}", 'user')

        ai_responses = []
        last_speaker = None  # iinitialize last_speaker to track who spoke previously

        for agent in agent_list:
            print(user_question)
            # get the response from the current agent
            response = agent.get_output(user_question[1])['message']['content']

            # If theres a last speaker, include their name in the response
            if last_speaker:
                formatted_response = f"{last_speaker}, {response}"
            else:
                formatted_response = response

            # Now asssign the current agent as the last speaker
            last_speaker = agent.name

            # store the response and update the chat
            user_question = (agent.name, formatted_response)

            for A in agent_list:
                if A != agent:
                    A.add_message(user_question[1], 'user')
                else:
                    A.add_message(f"{user_question[1]}", 'assistant')
            ai_responses.append(user_question)

        # Update the chat with AI responses
        for ai_response in ai_responses:
            self.update_chat(ai_response)

        # Clear the input box for next question
        self.prompt_entry.delete(0, tk.END)

    def update_chat(self, message):
        """
        A function to update the chat history with a new message.

        This method inserts a new message into the chat history, scrolls to the bottom,
        and disables editing of the chat history.

        :param message: The message to display in the chat
        :return: None
        """
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, f"\n\n{message[0]}: ", "bold")  # panelist name
        self.chat_history.insert(tk.END, message[1] + "\n", "normal")  # panelist message
        # self.chat_history.yview(tk.END)  # Auto-scroll to the bottom
        self.chat_history.config(state=tk.DISABLED)

    def clear_chat(self):
        """
        A function to clear the chat history.

        This method removes all the content from the chat history and disables editing.

        :return: None
        """
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.delete(1.0, tk.END)
        self.chat_history.config(state=tk.DISABLED)


def main():
    """
    Main function to run the Tkinter GUI.

    This function initializes the root window and starts the main event loop of the application.

    :return: None
    """
    root = tk.Tk()
    root.attributes('-topmost', True)  # window always on top

    # Prompt the user for their name
    username = simpledialog.askstring("Username selector", "Enter your name: ",)
    if not username:  # if blank, default to "User"
        username = "User"
    print(f"Selected username: {username}")

    # Prompt the user for the number of AI panelists
    num_agents = simpledialog.askinteger("Number of Panelists", "Enter the number of AI panelists:", minvalue=2, maxvalue=10)
    print(f"Selected number of panelists: {num_agents}")

    # Create the game instance
    game = AIPanelGame(root, agents=[], username=username)

    # Create AI panelists
    desc = "a panelist on a podcast discussing the user's topic. you keep the conversation going by asking questions to the others or the user. do not introduce yourself nor say your name."
    agent_list = [Agent(game.randomize_unique_names(), desc) for _ in range(num_agents)]
    game.agents = agent_list

    root.mainloop()


if __name__ == "__main__":  # main guard
    main()