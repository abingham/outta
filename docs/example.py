from outta.parser import Parser

# Here's the text to be parsed
text = "\x1b[4COut of\x1b[3Dta control!"

# Construct a Parser and feed the text in.
parser = Parser()
elements = list(parser.feed(text))

# Print each of the elements
for element in elements:
    print(">", element)

# Reconstruct the input text from the elements and print it
full_text = "".join(e.text for e in elements)
assert full_text == text
print(full_text)