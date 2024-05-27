# chatui.py -- UI for Conversational Interface to Local LLMs

# Conversational (https://github.com/foretspaisibles/conversational)
# This file is part Conversational.
#
# Copyright © 2024 Michaël Le Barbier
# All rights reserved.

# This file must be used under the terms of the MIT License.
# This source file is licensed as described in the file LICENSE, which
# you should have received as part of this distribution. The terms
# are also available at https://opensource.org/licenses/MIT

from tkinter import *
from tkinter import ttk

TEXT_WIDTH=60

def defineStyles(style):
    ttk.Style().configure("Dangerous.TLabel", background="red")
    ttk.Style().configure("DeveloperTool.TButton", padding=12, relief="flat", background="red")

class SystemInstructions(ttk.Frame):
    """A static widget displaying system instructions."""
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.instructions = kwargs['instructions']
        self.label = ttk.Label(self, text="System Instructions")
        self.text = Text(self, width=TEXT_WIDTH, height=10)
        self.text.insert(END, self.instructions)
        self.label.pack()
        self.text.pack(fill=BOTH, expand=True)

class Conversation(ttk.Frame):
    """A widget displaying a conversation."""
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.text = Text(self, width=TEXT_WIDTH, height=40)
        self.scrollbar = ttk.Scrollbar(self)

        self.scrollbar.config(command=self.text.yview)
        self.text.config(yscrollcommand=self.scrollbar.set, setgrid=1)
        self.querySeparator = ""
        self.text.tag_configure("query", font="Verdana 14 bold")
        self.text.tag_configure("reply", font="Verdana 14")
        self.text.pack(side=LEFT, fill=BOTH, expand=True)
        self.scrollbar.pack(side=RIGHT, fill=Y)

    def insertQuery(self, text):
        self.text.insert(END, self.querySeparator + text, ('query'))
        self.querySeparator = "\n\n\n"

    def insertReply(self, text):
        self.text.insert(END, "\n\n"+ text, ('reply'))

        
class Toolbar(ttk.Frame):
    """A widget displaying a toolbar."""
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.exportCommand=kwargs['exportCommand']
        self.quitCommand=kwargs['quitCommand']
        self.queryCommand=kwargs['queryCommand']
        self.quitbutton = ttk.Button(self, text="⚠️ Quit", command=self.quitCommand)
        self.export = ttk.Button(self, text="Export", command=self.exportCommand)
        self.query = ttk.Button(self, text="Query", command=self.queryCommand)
        for button in [self.quitbutton, self.export, self.query]:
            button.pack(side=LEFT, padx=2, pady=5)

        if kwargs.get('enableDeveloperTools', False):
            self.randomQuery = ttk.Button(self, text="👩‍💻 RandomQuery", command=(lambda : self.queryCommand(text="Some random text.")))
            self.randomQuery.pack(side=RIGHT, padx=2, pady=5)

class UserInput(ttk.Frame):
    """A widget for user input."""
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.text = Text(self, width=TEXT_WIDTH, height=10)
        self.text.pack(fill=BOTH, expand=True)

    def retrieve(self):
        userInput = self.text.get("1.0",'end-1c')
        self.text.delete("1.0",'end-1c')
        return userInput

class Application(ttk.Frame):
    """A conversational application."""
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent)
        self.instructions = SystemInstructions(self, instructions=kwargs['instructions'])
        self.exportCommand=kwargs['exportCommand']
        self.quitCommand=kwargs['quitCommand']
        self.queryCommand=kwargs['queryCommand']
        self.conversationLabel = ttk.Label(self, text="Conversation")
        self.conversation = Conversation(self)
        self.chat = [{'role': 'system', 'content': kwargs['instructions']}]
        self.toolbar = Toolbar(self, quitCommand=self.onQuit, exportCommand=self.onExport, queryCommand=self.onQuery, enableDeveloperTools=kwargs.get('enableDeveloperTools', False))
        self.userInputLabel = ttk.Label(self, text="User Input")
        self.userInput = UserInput(self)
        self.toolbar.pack(fill=X, expand=True)
        self.instructions.pack(fill=BOTH, expand=True)
        self.conversationLabel.pack()
        self.conversation.pack(fill=BOTH, expand=True)
        self.userInputLabel.pack()
        self.userInput.pack(fill=BOTH, expand=True)
        
    def onQuery(self, text=None):
        if text is None:
            text = self.userInput.retrieve()
        self.chat.append({'role': 'user', 'content': text})
        self.conversation.insertQuery(text)
        reply = self.queryCommand(text=text, chat=self.chat)
        self.chat.append({'role': 'assistent', 'content': reply})
        self.conversation.insertReply(reply)

    def onExport(self):
        self.exportCommand(self.chat)

    def onQuit(self):
        self.quitCommand()
