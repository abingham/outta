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

.. literalinclude:: docs/example.py

and here's how that look if you run it:

.. literalinclude:: docs/example.output