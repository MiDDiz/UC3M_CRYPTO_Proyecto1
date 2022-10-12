import tkinter as tk

# Simple library encrypted exercise.

def main():
    print("Hello")
    window = tk.Tk()
    label = tk.Label(
        text="CryptoNetflix",
        foreground="white",  # Set the text color to white
        background="grey"  # Set the background color to black
    )
    label.pack()
    window.mainloop()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
