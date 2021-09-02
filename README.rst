=====
outta
=====

A tool for parsing terminal control codes and escape sequences from a stream of 
text.

Outta was born out of a need to learn more about the control codes sent from terminal
programs to the terminals that host them. The ``Parser`` class can parse a stream
of text and produce a sequence of ``Element``\s that tell you what codes (and regular
text) were in it. 

Here's a quick example:

.. code-block:: python

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

and here's how that look if you run it:

.. code-block::

  % python docs/example.py
  > CursorForward(parameters=(4,), keywords={}, text='\x1b[4C')
  > Out of
  > CursorBack(parameters=(3,), keywords={}, text='\x1b[3D')
  > ta control!
      Outta control!
