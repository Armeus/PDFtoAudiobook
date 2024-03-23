# Imports
import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfReader
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir

# Create a client using the credentials and region defined in the [adminuser]
# section of the AWS credentials file (~/.aws/credentials).
session = Session(profile_name="adminuser")
polly = session.client("polly")


class App(tk.Frame):
    # Initialize GUI with using Tkinter
    def __init__(self, parent):
        # Create buttons used
        super().__init__()
        self.text = ''
        self.button = tk.Button(parent, text='Select File', command=self.file_select,
                                     width=10, height=2, background='light grey')
        self.button.pack()

    # Prompts user to select initial pdf file
    def file_select(self):
        try:
            # On button click will prompt user to select a pdf file
            filename = filedialog.askopenfilename(defaultextension='.pdf', filetypes=[('pdf file', '.pdf')])
            # Update self.text with text from pdf file
            reader = PdfReader(filename)
            for n in range(len(reader.pages)):
                page = reader.pages[n]
                self.text += page.extract_text()
            self.convert_text()

        except AttributeError:
            tk.messagebox.showerror(title='Error', message='No File Selected')

    def convert_text(self):
        try:
            # Request speech synthesis
            response = polly.synthesize_speech(Text=self.text, OutputFormat="mp3",
                                               VoiceId="Joanna")
        except (BotoCoreError, ClientError) as error:
            # The service returned an error, exit gracefully
            print(error)
            sys.exit(-1)

        # Access the audio stream from the response
        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                output = os.path.join('.\output', "speech.mp3")

                try:
                    # Open a file for writing the output as a binary stream
                    with open(output, "wb") as file:
                        file.write(stream.read())
                except IOError as error:
                    # Could not write to file, exit gracefully
                    print(error)
                    sys.exit(-1)

        else:
            # The response didn't contain audio data, exit gracefully
            print("Could not stream audio")
            sys.exit(-1)

        # Play the audio using the platform's default player
        if sys.platform == "win32":
            os.startfile(output)
        else:
            # The following works on macOS and Linux. (Darwin = mac, xdg-open = linux).
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, output])


def main():
    root = tk.Tk()
    root.title("PDF to Audiobook Converter")
    root.minsize(width=500, height=300)
    root.config(padx=20, pady=20, background='grey')
    App(root).pack(expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()