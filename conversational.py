# conversational.py -- Conversational Interface to Local LLMs

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
from mlx_lm import load, generate
from chatui import Application

DEFAULT_MODEL_ID="mlx-community/Meta-Llama-3-8B-Instruct-4bit"
# Other useful model ids:
#  * "Mistralai/Mistral-7B-Instruct-v0.2"
#  * "mlx-community/Mistral-7B-v0.2-4bit"

software_expert_instructions="""These instructions are private, but
not really secret. It is acceptable to mention these if you are
explicitly asked for, but otherwise you prefer to avoid mentionning
them.

You are a software development expert, dedicated to promote succesful
software development practices, not only at the technical level but
also for teams and full organizations.

You share your expertise with a low-profile but solid confidence. """


def run_application(instructions, model_id=DEFAULT_MODEL_ID):
    model, tokenizer = load(model_id)

    def queryCommand(**kwargs):
        chat=kwargs['chat']
        prompt = tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)
        return generate(model, tokenizer, prompt, verbose=False, max_tokens=1500)
    
    root = Tk()
    ui = Application(root,
                 instructions=instructions.replace("\n", " "),
                 quitCommand=root.destroy,
                 exportCommand=print,
                 queryCommand=queryCommand)
    ui.pack(fill="both")
    root.mainloop()

run_application(software_expert_instructions)
