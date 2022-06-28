#!/usr/bin/env python

"""sutori.py: A simple to use dialog system for websites, apps, games and more."""

__author__ = "Kodaloid (Steve Bailey)"
__copyright__ = "Copyright 2022, The Sutori Project"
__license__ = "MIT"
__version__ = "0.0.1"


import xml.dom.minidom;
from enum import Enum;



class SutoriCulture(str, Enum):
	NONE = 'none'
	ALL = 'all'
	EN_US = 'en-US' # English (United States)
	ZH_CN = 'zh-CN' # Chinese (simplified, PRC)
	RU_RU = 'ru-RU' # Russian (Russia)
	FR_FR = 'fr-FR' # French (France)
	ES_ES = 'es-ES' # Spanish (Spain)
	EN_GB = 'en-GB' # English (United Kingdom)
	DE_DE = 'de-DE' # German (Germany)
	PT_BR = 'pt-BR' # Portuguese (Brazil)
	EN_CA = 'en-CA' # English (Canada)
	ES_MX = 'es-MX' # Spanish (Mexico)
	IT_IT = 'it-IT' # Italian (Italy)
	JA_JP = 'ja-JP' # Japanese (Japan)}


class SutoriSolver(str, Enum):
	NONE = 'none'
	OPTION_INDEX = 'option_index'
	KEY_CHAR_EQUALITY = 'key_char_equality'
	TEXT_EQUALITY = 'text_equality'
	CUSTOM = 'custom'




class SutoriTools:
	def read_attr(xml_node, name, default = ""):
		if xml_node.hasAttribute(name):
			_attr = xml_node.getAttribute(name)
			return _attr;
		return default
		
	def read_attr_culture(xml_node, name, default = SutoriCulture.NONE):
		if xml_node.hasAttribute(name):
			_attr = xml_node.getAttribute(name)
			return SutoriCulture(_attr);
		return default

	def read_attrs(xml_node, exclude_list):
		_res = {}
		for _key in xml_node.attributes.keys():
			if not _key in exclude_list:
				_res[_key] = xml_node.getAttribute(_key)
		return _res



# A loader provides sutori the ability to load xml from places, override it
# with your own if you wish to add extra abilities to this.
class SutoriLoader:
	def load(self, file):
		f = open(file, 'r')
		_result = f.read()
		f.close()
		return _result



class SutoriInclude:
	path = ""
	after = False
	def __init__(self, xml_node):
		self.path = SutoriTools.read_attr(xml_node, 'path')
		self.after = SutoriTools.read_attr(xml_node, 'after') == "true"



class SutoriResourceImage:
	id = ""
	name = ""
	src = ""
	preload = False
	def __init__(self, xml_node):
		self.id = SutoriTools.read_attr(xml_node, 'id')
		self.name = SutoriTools.read_attr(xml_node, 'name')
		self.src = SutoriTools.read_attr(xml_node, 'src')
		self.preload = SutoriTools.read_attr(xml_node, 'preload') == "true"




class SutoriActor:
	attributes = {}
	elements = []
	id = ""
	name = ""
	culture = SutoriCulture.NONE
	def __init__(self, xml_node):
		self.id = SutoriTools.read_attr(xml_node, 'id')
		self.name = SutoriTools.read_attr(xml_node, 'name')
		self.culture = SutoriTools.read_attr(xml_node, 'lang')



class SutoriMoment(object):
	attributes = {}
	elements = []
	actor = ""
	clear = False
	goto = ""
	id = ""
	def __init__(self, xml_node):
		self.id = SutoriTools.read_attr(xml_node, 'id')
		_elements = []
		for _element in xml_node.childNodes:
			if _element.nodeType is _element.ELEMENT_NODE:
				if _element.tagName == 'text':
					_elements.append(SutoriElementText(_element))
				elif _element.tagName == 'image':
					_elements.append(SutoriElementImage(_element))
				elif _element.tagName == 'option':
					_elements.append(SutoriElementOption(_element))
		self.elements = _elements
		self.actor = SutoriTools.read_attr(xml_node, 'actor')
		self.clear = SutoriTools.read_attr(xml_node, 'clear') == 'true'
		self.goto = SutoriTools.read_attr(xml_node, 'goto')
		self.id = SutoriTools.read_attr(xml_node, 'id')
		self.attributes = SutoriTools.read_attrs(xml_node, ['actor', 'clear', 'goto', 'id'])

	def get_text(self, culture):
		for _element in self.elements:
			if isinstance(_element, SutoriElementText):
				if _element.culture == culture:
					return _element.text
		return ''

	def get_options(self, culture):
		_res = []
		for _element in self.elements:
			if isinstance(_element, SutoriElementOption):
				if _element.culture == culture:
					_res.append(_element)
		return _res



class SutoriElement(object):
	attributes = {}
	culture = SutoriCulture.NONE



class SutoriElementText(SutoriElement):
	text = ""
	def __init__(self, xml_node):
		self.text = xml_node.firstChild.data
		self.culture = SutoriTools.read_attr_culture(xml_node, 'lang')
		self.attributes = SutoriTools.read_attrs(xml_node, ['lang'])



class SutoriElementOption(SutoriElement):
	text = ""
	target = ""
	solver = SutoriSolver.NONE
	solver_callback = ""
	def __init__(self, xml_node):
		self.text = xml_node.firstChild.data
		self.target = SutoriTools.read_attr(xml_node, "target")
		self.solver = SutoriTools.read_attr(xml_node, "solver")
		self.solver_callback = SutoriTools.read_attr(xml_node, "solver_callback")
		self.culture = SutoriTools.read_attr_culture(xml_node, 'lang')
		self.attributes = SutoriTools.read_attrs(xml_node, ['target', 'solver', 'solver_callback', 'lang'])



class SutoriElementImage(SutoriElement):
	actor = ""
	used_for = None
	resource_id = ""
	def __init__(self, xml_node):
		self.actor = SutoriTools.read_attr(xml_node, 'actor')
		self.used_for = SutoriTools.read_attr(xml_node, "for")
		self.resource_id = SutoriTools.read_attr(xml_node, 'resource')
		self.culture = SutoriTools.read_attr(xml_node, 'lang')
		self.attributes = SutoriTools.read_attrs(xml_node, ['actor', 'for', 'resource', 'lang'])



class SutoriDocument(object):
	properties = {}
	resources = []
	actors = []
	moments = []
	includes = []
	uri_loader = None


	def __init__(self):
		self.uri_loader = SutoriLoader()


	# Load a Sutori XML file
	def load_xml_file(self, file, load_includes = True):
		_code = self.uri_loader.load(file);
		# load the xml file.
		_xml = xml.dom.minidom.parseString(_code);
		# get the <document> node.
		_doc = _xml.firstChild

		# load the properties.
		_props = _doc.getElementsByTagName('properties')
		if _props.length > 0:
			for _prop in _props[0].childNodes:
				if _prop.nodeType is _prop.ELEMENT_NODE:
					self.properties[_prop.tagName] = _prop.firstChild.data

		# load the includes.
		_includes = _doc.getElementsByTagName('include');
		if _includes.length > 0:
			for _include in _includes.childNodes:
				if _include.nodeType is _include.ELEMENT_NODE:
					_includeObj = SutoriInclude(_include)
					if load_includes == True and _includeObj.after == False:
						print('todo: Load include!!')
					self.includes.append(_includeObj)

		# load the resources.
		_resources = _doc.getElementsByTagName('resources')
		if _resources.length > 0:
			for _resource in _resources[0].childNodes:
				if _resource.nodeType is _resource.ELEMENT_NODE:
					if _resource.tagName == 'image':
						self.resources.append(SutoriResourceImage(_resource))

		# load actors.
		_actors = _doc.getElementsByTagName('actors')
		if _actors.length > 0:
			for _actor in _actors[0].childNodes:
				if _actor.nodeType is _resource.ELEMENT_NODE and _actor.tagName == 'actor':
					self.actors.append(SutoriActor(_actor))

		# load moments.
		_moments = _doc.getElementsByTagName('moments')
		if _moments.length > 0:
			for _moment in _moments[0].childNodes:
				if _moment.nodeType is _moment.ELEMENT_NODE and _moment.tagName == 'moment':
					self.moments.append(SutoriMoment(_moment))

		# load any includes that had after set to true
		for _includeObj in self.includes:
			if load_includes == True and _includeObj.after == True:
				print('todo: Load include after!!')
	

	# Get a moment by id.
	def get_moment_by_id(self, id):
		for _moment in self.moments:
			if _moment.id == id:
				return _moment
		return None


	# Get a resource by id.
	def get_resource_by_id(self, id):
		for _resource in self.resources:
			if _resource.id == id:
				return _resource
		return None



class SutoriEngine(object):
	cursor = None
	document = None
	challenge_event = None
	end_event = None

	def __init__(self, doc):
		self.document = doc

	def goto_moment_id(self, moment_id): 
		_moment = self.document.get_moment_by_id(moment_id)
		if _moment == None: raise Exception("Could not find moment with id #"+moment_id+".")
		self.goto_moment(_moment)

	def goto_moment(self, moment):
		if moment == None: moment = self.document.moments[0]
		if moment == None: raise Exception("Document does not have any moments!")
		self.cursor = moment
		if callable(self.challenge_event):
			self.challenge_event(moment)
	
	def play(self):
		self.goto_moment(None)

	def goto_next_moment(self):
		if self.cursor == None: return
		_index = self.document.moments.index(self.cursor)
		if _index == -1: return

		# if the moment has a goto, use that instead.
		if self.cursor.goto != '':
			self.goto_moment_id(self.cursor.goto)
			return
		# handle reaching the end.
		if _index == len(self.document.moments) - 1:
			if (callable(self.end_event)):
				self.end_event()
			return
		# if we get to this point, we really wanna go to the next moment.
		self.goto_moment(self.document.moments[_index + 1])