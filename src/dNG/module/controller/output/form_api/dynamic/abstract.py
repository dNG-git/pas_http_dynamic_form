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

from binascii import hexlify
from os import urandom

from dNG.controller.predefined_http_request import PredefinedHttpRequest
from dNG.data.binary import Binary
from dNG.data.text.input_filter import InputFilter
from dNG.data.text.l10n import L10n
from dNG.data.xhtml.form.processor import Processor as FormProcessor
from dNG.data.xhtml.link import Link
from dNG.data.xhtml.oset.file_parser import FileParser
from dNG.data.xml_parser import XmlParser
from dNG.database.connection import Connection
from dNG.module.controller.services.abstract_dom_editor import AbstractDomEditor
from dNG.runtime.not_implemented_exception import NotImplementedException

class Abstract(AbstractDomEditor):
#
	"""
"Abstract" is used to handle dynamic form input fields.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: dynamic_form
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
	"""

	def _apply_edit_form(self, form):
	#
		"""
Applies changes to the edit form.

:param form: Form to add fields to

:since: v0.1.00
		"""

		self._apply_form(form)
	#

	def _apply_form(self, form):
	#
		"""
Applies changes to the form.

:param form: Form to add fields to

:since: v0.1.00
		"""

		raise NotImplementedException()
	#

	def _apply_new_form(self, form):
	#
		"""
Applies changes to the new form.

:param form: Form to add fields to

:since: v0.1.00
		"""

		self._apply_form(form)
	#

	def _get_empty_view_content(self):
	#
		"""
Returns content for an empty dynamic field.

:return: (str) Valid XHTML form field content for an empty dynamic field
:since:  v0.1.00
		"""

		status_attributes = ({ "tag": "div",
		                       "attributes": { "class": "pageform_error" },
		                       "value": L10n.get("pas_http_core_form_error_required_element")
		                     }
		                     if (self.request.get_dsd("oform_field_required") == "1") else
		                     { "tag": "div",
		                       "value": L10n.get("pas_http_core_form_element_entry_empty")
		                     }
		                    )

		return XmlParser().dict_to_xml_item_encoder(status_attributes)
	#

	def _get_formatted_entry_content(self, entry_position, template_name, content):
	#
		"""
@TODO
		"""

		file_parser = FileParser()
		entry_content = file_parser.render(template_name, content)

		link = Link()

		delete_query_string = link.build_url(Link.TYPE_QUERY_STRING, { "__request__": True,
		                                                               "a": "delete",
		                                                               "dsd": { "oform_field_entry_position": entry_position }
		                                                             }
		                                    )

		edit_query_string = link.build_url(Link.TYPE_QUERY_STRING, { "__request__": True,
		                                                             "a": "edit",
		                                                             "dsd": { "oform_field_entry_position": entry_position }
		                                                           }
		                                  )

		content = { "content": entry_content,
		            "edit_query_string": edit_query_string,
		            "delete_query_string": delete_query_string
		          }

		return file_parser.render("dynamic_form.field_entry", content)
	#

	def _get_form_action_edit_title(self):
	#
		"""
@TODO
		"""

		return L10n.get("pas_http_core_form_element_entry_edit")
	#

	def _get_form_action_new_title(self):
	#
		"""
@TODO
		"""

		return L10n.get("pas_http_core_form_element_entry_new")
	#

	def _get_form_field_list(self):
	#
		"""
@TODO
		"""

		form_field_id = InputFilter.filter_control_chars(self.request.get_dsd("oform_field_id"))

		form_value_dict = self._get_form_store().get_value_dict()
		return form_value_dict.get("form_api_dynamic_{0}".format(form_field_id), [ ])
	#

	def _get_form_store(self):
	#
		"""
@TODO
		"""

		form_id = InputFilter.filter_control_chars(self.request.get_dsd("oform_id"))
		return FormProcessor.load_form_store_id(form_id)
	#

	def _get_new_entry_link_content(self):
	#
		"""
@TODO
		"""

		query_string = Link().build_url(Link.TYPE_QUERY_STRING, { "__request__": True, "a": "new" })

		link_attributes = { "tag": "a",
		                    "attributes": { "data-pas-dom-editor-query": query_string, "href": "" },
		                    "value": L10n.get("pas_http_core_form_element_entry_new")
		                  }

		return "<p>{0}</p>".format(XmlParser().dict_to_xml_item_encoder(link_attributes))
	#

	def _get_view_content(self, entry_list):
	#
		"""
Returns (X)HTML for the current content of an dynamic field.

:return: (str) Valid XHTML form field content for an dynamic field
:since:  v0.1.00
		"""

		raise NotImplementedException()
	#

	@Connection.wrap_callable
	def execute_get(self):
	#
		"""
Action for "get"

:since: v0.1.00
		"""

		L10n.init("pas_http_core_form")

		entry_list = self._get_form_field_list()

		self._set_replace_dom_result("<div>{0}\n{1}</div>".format(self._get_view_content(entry_list),
		                                                          self._get_new_entry_link_content()
		                                                         ),
		                             on_replaced = "pas/HttpJsonApiDomEditor.min",
		                             type = "link_activated"
		                            )
	#

	@Connection.wrap_callable
	def execute_delete(self):
	#
		"""
Action for "delete"

:since: v0.1.00
		"""

		form_field_id = InputFilter.filter_control_chars(self.request.get_dsd("oform_field_id", "")).strip()
		form_field_entry_position = InputFilter.filter_int(self.request.get_dsd("oform_field_entry_position", -1))

		if (form_field_entry_position > -1):
		#
			form_store = self._get_form_store()
			form_store_dict = form_store.get_value_dict()
			form_store_field_id = "form_api_dynamic_{0}".format(form_field_id)

			entry_list = form_store_dict.get(form_store_field_id, [ ])
			if (len(entry_list) > form_field_entry_position): del(entry_list[form_field_entry_position])

			form_store_dict[form_store_field_id] = entry_list
			form_store.set_value_dict(form_store_dict)
		#

		redirect_request = PredefinedHttpRequest()
		redirect_request.set_module(self.request.get_module())
		redirect_request.set_service(self.request.get_service())
		redirect_request.set_action("get")
		redirect_request.set_dsd_dict(self.request.get_dsd_dict())

		self.request.redirect(redirect_request)
	#

	@Connection.wrap_callable
	def execute_edit(self, is_save_mode = False):
	#
		"""
Action for "edit"

:since: v0.1.00
		"""

		form_id = InputFilter.filter_control_chars(self.request.get_dsd("oform_id", "")).strip()

		L10n.init("pas_http_core_form")

		form = FormProcessor(form_id)
		form.set_form_render_id(Binary.str(hexlify(urandom(16))))

		if (is_save_mode): form.set_input_available()

		self._apply_edit_form(form)

		if (is_save_mode and form.check()):
		#
			self._save_edit_form(form)
			self._set_destroy_dom_result()
		#
		else:
		#
			content = { "title": self._get_form_action_edit_title(),
			            "on_closed_query": Link().build_url(Link.TYPE_QUERY_STRING, { "__request__": True, "a": "get" })
			          }

			content['form'] = { "object": form,
			                    "url_parameters": { "__request__": True,
			                                        "a": "edit-save"
			                                      },
			                    "button_title": "core_continue"
			                  }

			method = (self._set_replace_dom_oset_result
			          if (is_save_mode) else
			          self._set_append_overlay_dom_oset_result
			         )

			method("dynamic_form.overlay", content)
		#
	#

	def execute_edit_save(self):
	#
		"""
Action for "edit-save"

:since: v0.1.00
		"""

		self.execute_edit(self.request.get_type() == "POST")
	#

	@Connection.wrap_callable
	def execute_new(self, is_save_mode = False):
	#
		"""
Action for "new"

:since: v0.1.00
		"""

		form_id = InputFilter.filter_control_chars(self.request.get_dsd("oform_id", "")).strip()
		form_field_id = InputFilter.filter_control_chars(self.request.get_dsd("oform_field_id", "")).strip()

		L10n.init("pas_http_core_form")

		form = FormProcessor(form_id)
		form.set_form_render_id(Binary.str(hexlify(urandom(16))))

		if (is_save_mode): form.set_input_available()

		self._apply_new_form(form)

		if (is_save_mode and form.check()):
		#
			entry_data = self._save_new_form(form)

			form_store = form.get_form_store()
			form_store_dict = form_store.get_value_dict()
			form_store_field_id = "form_api_dynamic_{0}".format(form_field_id)

			entry_list = form_store_dict.get(form_store_field_id, [ ])
			entry_list.append(entry_data)

			form_store_dict[form_store_field_id] = entry_list
			form_store.set_value_dict(form_store_dict)

			self._set_destroy_dom_result()
		#
		else:
		#
			content = { "title": self._get_form_action_new_title(),
			            "on_closed_query": Link().build_url(Link.TYPE_QUERY_STRING, { "__request__": True, "a": "get" })
			          }

			content['form'] = { "object": form,
			                    "url_parameters": { "__request__": True,
			                                        "a": "new-save"
			                                      },
			                    "button_title": "core_continue"
			                  }

			method = (self._set_replace_dom_oset_result
			          if (is_save_mode) else
			          self._set_append_overlay_dom_oset_result
			         )

			method("dynamic_form.overlay", content)
		#
	#

	def execute_new_save(self):
	#
		"""
Action for "new-save"

:since: v0.1.00
		"""

		self.execute_new(self.request.get_type() == "POST")
	#

	def _save_edit_form(self, form):
	#
		"""
Handles and returns data to be saved for an edited dynamic form entry.

:return: (mixed) Changed data to be saved for the edited dynamic entry
:since:  v0.1.00
		"""

		raise NotImplementedException()
	#

	def _save_new_form(self, form):
	#
		"""
Handles and returns data to be saved as a new dynamic form entry.

:return: (mixed) Data to be saved for the new dynamic entry
:since:  v0.1.00
		"""

		raise NotImplementedException()
	#
#

##j## EOF