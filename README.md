# Conversational

A simple conversational interface to a local LLM. This requires the
packages `mlx-llm` and `tkinter` as well as an account to HuggingFace,
so as to download the models.

The UI is very bad and this has been put together in a couple of
hours.

== How to use

 * Start with `python3.x conversational.py`
 * In the UI enter your question in the text frame at the bottom.
 * When you are ready, hit the `Query` buttin in the toolbar, so that
   the LLM can produce an answer. 
   the UI will freeze for a second.
 * If the conversation is interesting, the `Export` button will print
   it to the terminal.
 * When you are done, hit the `Quit` button.
