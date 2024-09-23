"""
Ollama
09/23/24
Quang Huynh
"""

import tkinter as tk
from tkinter import scrolledtext
import ollama as o

def chat(prompt, name):
    """
    A function that gets the A.I. response

    :param prompt: The user inputted prompt
    :param name: Name of current A.I. talking
    :return: A formatted string with the AI's response
    """
    response = o.chat(model="dolphin-llama3", messages=[
        {
            'role': 'user',
            'content': prompt
        },
    ])
    return f"{name}: {response['message']['content']}"


class AIPanelGame:
    def __init__(self, root):
        """
        A class representing the AI Panel Game GUI.
        This class handles the main functionality of the game, including accepting user input,
        displaying responses from AI panelists, and managing the chat history.

        :param root: The root window of the Tkinter application
        """
        self.root = root
        self.root.title("AI Panel Game")

        # Instructions label
        self.instructions = tk.Label(root, text="Ask a question to the AI panelists:")
        self.instructions.pack(pady=5)

        # User input box
        self.prompt_entry = tk.Entry(root, width=100)
        self.prompt_entry.pack(pady=10)

        # Submit button
        self.submit_button = tk.Button(root, text="Submit", command=self.ask_question)
        self.submit_button.pack(pady=5)

        # Scrolled text box for chat history
        self.chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=20)
        self.chat_history.pack(pady=10)
        self.chat_history.config(state=tk.DISABLED)  # Disable typing in the chat history

        # Clear button
        self.clear_button = tk.Button(root, text="Clear", command=self.clear_chat)
        self.clear_button.pack(pady=5)


    def ask_question(self):
        """
        A function to handle user input and display AI responses.

        This method gets the user's question, sends it to multiple AI panelists,
        and updates the chat history with the responses.

        :return: None
        """
        user_question = self.prompt_entry.get()
        if user_question.strip() == "":
            return  # Don't process empty questions

        # Display the user's question in the chat
        self.update_chat("User (Moderator): " + user_question)

        # Get AI responses from panelists
        ai_response1 = chat(user_question, "Panelist 1")
        ai_response2 = chat(user_question, "Panelist 2")

        # Update the chat with AI responses
        self.update_chat(ai_response1)
        self.update_chat(ai_response2)

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
        self.chat_history.insert(tk.END, message + "\n")
        self.chat_history.yview(tk.END)  # Auto-scroll to the bottom
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
    game = AIPanelGame(root)
    root.mainloop()


if __name__ == "__main__":  # main guard
    main()