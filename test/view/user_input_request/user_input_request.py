import tkinter as tk

from src.view.user_input_request.user_input_request import UserInputRequestFacade


def ask() -> bool:
    user_input_request = UserInputRequestFacade()
    result = user_input_request.ask_acceptance("Do you want to continue?", "Continue?", "Title")
    return result


if __name__ == "__main__":
    root_window = tk.Tk()
    ask_button = tk.Button(master=root_window, text="Ask", command=lambda: print(ask()))
    ask_button.pack()
    root_window.mainloop()
