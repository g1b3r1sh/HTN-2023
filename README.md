# HackTheNorth 2023

The premise of my hack is utilising LLMs to generate image macros given a topic.
By using the fact that image macros often contain the same image and follow the same format, similar examples can be easily extracted so that the LLM can generate a new macro.

First, given a dataset of macros based on a single image, each macro is passed through a text extractor, giving us several examples we can give the LLM.

To generate a meme about a given topic, we pass examples together with the topic to generate a new image macro about that topic.

# Updates

- In the interest of time and output quality, this hack will only process image macros that have a "top-text-bottom-text" format
- For improved output quality, the user will input the top text, and the program generates bottom text
