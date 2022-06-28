# sutori-py

A simple to use Python dialog system for websites, apps, games and more.



## Introduction

Sutori is a dialog engine that enables you to add an easy to customise dialog
abilities to nearly anything that needs them. Here are some great examples of
use cases:

- A quiz/survey on a website.
- Custom checkout process for buying things on a web shop.
- Conversation system in computer game.
- Visual novel creation.
- Telephone switch board.

Dialog is written in XML files, with a structure that allows for multiple
languages, option branches, multimedia (images, audio, video). Dialog is
broken up into a list of moments in which the conversation can traverse.

Here is an example of a basic sutori XML document:

```xml
<?xml version="1.0" encoding="utf-8"?>
<document xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xmlns:xsd="http://www.w3.org/2001/XMLSchema">
   <moments>
      <moment>
         <text>Which door do you want to open?</text>
         <option target="door1">Door 1</option>
         <option target="door2">Door 2</option>
      </moment>

      <moment id="door1" clear="true" goto="end">
         <text>You picked door1</text>
      </moment>

      <moment id="door2" clear="true" goto="end">
         <text>You picked door2</text>
      </moment>

      <moment id="end">
         <text>This is the end</text>
      </moment>
   </moments>
</document>
```

Sutori closely mimics the way [CYOA (choose your own adventure)](https://en.wikipedia.org/wiki/Gamebook)
Gamebooks work, with the small difference is that at the end of each moment, the
user is asked what to do next.



## Sister Projects

- [sutori-studio](https://github.com/sutori-project/sutori-studio) - An IDE for editing Sutori XML files.
- [sutori-game](https://github.com/sutori-project/sutori-game) - A template for creating basic visual novels with sutori-js.
- [sutori-js](https://github.com/sutori-project/sutori-js) - The JavaScript version of Sutori engine.
- [sutori-cs](https://github.com/sutori-project/sutori-cs) - The .NET Standard 2.0 version of Sutori engine.



## This Repo

This repository is the Python implementation of the Sutori dialog engine. If is
written to be compatible with Python 3+. There is no compiling needed to use
this version, just copy `sutori.py` into your work folder, and reference it like
any other module: 

If you wish to try the example. Clone this repo, then navigate to the folder on
your local machine in a terminal, and type:

`
python ./example1.py
`

Why not try modifying example1.xml to add more to the story.


## How To Use Sutori

Here's a bare bones example of how to setup a Sutori project in Python: 


```python
import sutori;

# load document
doc = sutori.SutoriDocument()
doc.load_xml_file("example1.xml")

# init the engine.
engine = sutori.SutoriEngine(doc)

# choose a culture (language)
culture = sutori.SutoriCulture.NONE

# create handler for challenge events
def handle_challenge(moment):
	
   _options = moment.get_options(culture)
	
   if len(_options) > 0:
		for _option in _options:
			print("-- " + _option.text)
		response = input(moment.get_text(culture) + ' ')
		if response == '1': engine.goto_moment_id(_options[0].target)
		if response == '2': engine.goto_moment_id(_options[1].target)
		if response == '3': engine.goto_moment_id(_options[1].target)
	
   else:
		input(moment.get_text(culture) + ' ')
		engine.goto_next_moment()

# create handler for end event.
def handle_end():
	print('-- fin --')

# hook the events into the engine, then begin.
engine.challenge_event = handle_challenge
engine.end_event = handle_end
engine.play()
```


## Conclusion

This was created originally to figure out how to add branched sequencing to the
Xentu game engine. However it turns out Sutori has a lot of uses in other
situations too.

Thanks for checking out the project, and I hope you find it useful.

Kodaloid