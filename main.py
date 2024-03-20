# Imports
import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfReader


class App(tk.Frame):
    # Initialize GUI with using Tkinter
    def __init__(self, parent):
        # Create buttons used
        super().__init__()
        self.text = ''
        self.button = tk.Button(parent, text='Select File', command=self.file_select,
                                     width=10, height=2, background='light grey')
        self.button.pack()

    # Prompts user to select initial image and updates GUI for next step
    def file_select(self):
        try:
            # On button click will prompt user to select a pdf file
            filename = filedialog.askopenfilename(defaultextension='.pdf', filetypes=[('pdf file', '.pdf')])
            # Update self.text with text from pdf file
            reader = PdfReader(filename)
            for n in range(len(reader.pages)):
                page = reader.pages[n]
                self.text += page.extract_text()
        except AttributeError:
            tk.messagebox.showerror(title='Error', message='No File Selected')


def main():
    root = tk.Tk()
    root.title("PDF to Audiobook Converter")
    root.minsize(width=500, height=300)
    root.config(padx=20, pady=20, background='grey')
    App(root).pack(expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()