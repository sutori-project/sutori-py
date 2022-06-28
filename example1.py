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