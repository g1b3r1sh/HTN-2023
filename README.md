# HackTheNorth 2023

The premise of my hack is utilising LLMs to generate image macros given a topic.
By using the fact that image macros often contain the same image and follow the same format, similar examples can be easily extracted so that the LLM can generate a new macro.

First, given a dataset of macros based on a single image, each macro is passed through a text extractor, giving us several examples we can give the LLM.

To generate a meme about a given topic, we pass examples together with the topic to generate a new image macro about that topic.

# Updates

- In the interest of time and output quality, this hack will only process image macros that have a "top-text-bottom-text" format
- For improved output quality, the user will input the top text, and the program generates bottom text

## What it does
An image macro is a form of internet meme where text is added onto specific images. While they are often used for humour, they can also be used for other purposes such as marketing.

This project allows the user to generate their own macros which promote a product. First, the user gives several example macros which originate from a template image. Then, the user inputs the product name and "top text" of the macro they want to generate. By using the examples together with the input data, an LLM can produce a new macro in a format similar to the examples that promotes the product.
## How we built it
There are two parts to this project:
- Extracting the text from examples: By performing several manipulations on the example image using the template image, the text can be isolated enough for it to parsed by an OCR with great accuracy.
- Generating the new macro with an LLM: Through reading articles and trial and error, several insights into generating pattern-based output were found:
  - At the beginning of the prompt, state the purpose (ex. `Generate a viral image macro...`)
  - Use adjectives to make small adjustments to the output and define any words which may cause confusion to the LLM (ex. `...a viral image macro advertising the product "[PRODUCT NAME]"`)
  - Make sure the examples are clearly defined (ex. 
```
...in a similar format to the examples.

Top Text: [EXAMPLE TEXT]...
```
)
  - At the end, insert an incomplete example for the LLM to fill in (ex.
```
...[EXAMPLES]

Top Text: [USER INPUT]
Bottom Text:
```
)
  - Ellipses can be used to encourage the LLM to complete a phrase from a previous line (ex.
```
...
Top Text: HAVE A [PRODUCT NAME]...
Bottom Text: "
```
)
## Challenges we ran into
In the end, most of the time was spent writing the image processing and LLM code, leaving little to no time to write a front-end. Over the course of 3 long hours, a barely-functioning front-end was cobbled together.

## What's next for Marketing Meme Generator
Maybe in the future, all internet content will be generated through processes like this :D
