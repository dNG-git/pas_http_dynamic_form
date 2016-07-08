# -*- coding: utf-8 -*-
##j## BOF

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?pas;http;dynamic_form

The following license agreement remains valid unless any additions or
changes are being made by direct Netware Group in a written form.

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc.,
59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;gpl
----------------------------------------------------------------------------
#echo(pasHttpDynamicFormVersion)#
#echo(__FILEPATH__)#
"""

from dNG.data.text.input_filter import InputFilter
from dNG.data.http.translatable_exception import TranslatableException
from dNG.data.xhtml.form.processor import Processor
from dNG.data.xml_parser import XmlParser
from dNG.database.connection import Connection
from dNG.database.nothing_matched_exception import NothingMatchedException
from dNG.module.controller.services.abstract_dom_editor import AbstractDomEditor
from dNG.runtime.not_implemented_exception import NotImplementedException
from dNG.runtime.io_exception import IOException

class Abstract(AbstractDomEditor):
#
	"""
"Abstract" is used to handle dynamic form choices.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: dynamic_form
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
	"""

	@Connection.wrap_callable
	def execute_get(self):
	#
		"""
Action for "get"

:since: v0.1.00
		"""

		if (not self.response.is_supported("dict_result_renderer")): raise IOException("Unsupported response object for action")
		form_id = InputFilter.filter_control_chars(self.request.get_dsd("oform_id"))
		form_field_id = InputFilter.filter_control_chars(self.request.get_dsd("oform_field_id"))

		try: form_store = Processor.load_form_store_id(form_id)
		except NothingMatchedException as handled_exception: raise TranslatableException("core_access_denied", 403, _exception = handled_exception)

		self._handle_get_choices(form_store, form_field_id)
	#

	def execute_index(self):
	#
		"""
Action for "index"

:since: v0.1.00
		"""

		self.execute_get()
	#

	def _handle_get_choices(self, form_store, form_field_id):
	#
		"""
Handle calls to get the (continued) list of choices.

:return: (list) List of options
:since:  v0.1.00
		"""

		raise NotImplementedException()
	#

	def _render_choices_list(self, choices_list):
	#
		"""
Renders the given list of choices as (X)HTML content.

:since: v0.1.00
		"""

		_return = ""

		for choice_data in choices_list:
		#
			_return += XmlParser().dict_to_xml_item_encoder({ "tag": "option",
			                                                  "attributes": { "value": choice_data['value'] },
			                                                  "value": choice_data['title']
			                                                })
		#

		return _return
	#

	def _set_choices_result(self, choices_list, is_list_complete = False):
	#
		"""
Sets the choices result.

:since: v0.1.00
		"""

		self._set_append_dom_result(self._render_choices_list(choices_list),
		                            is_list_complete = is_list_complete
		                           )
	#
#

##j## EOF