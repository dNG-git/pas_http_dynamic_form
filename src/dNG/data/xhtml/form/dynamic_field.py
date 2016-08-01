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
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;gpl
----------------------------------------------------------------------------
#echo(pasHttpDynamicFormVersion)#
#echo(__FILEPATH__)#
"""

from dNG.data.xhtml.formatting import Formatting
from dNG.data.xhtml.link import Link
from dNG.runtime.value_exception import ValueException

from .abstract_field import AbstractField

class DynamicField(AbstractField):
#
	"""
"DynamicField" is used to provide more complex input use cases e.g. handling
multiple rows.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: dynamic_form
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
	"""

	def __init__(self, name = None):
	#
		"""
Constructor __init__(DynamicField)

:param name: Form field name

:since: v0.1.00
		"""

		AbstractField.__init__(self, name)

		self.dynamic_api_service = None
		"""
Service API endpoint for the dynamic input field.
		"""
		self.dynamic_api_service_parameters = None
		"""
Additional parameters transmitted at each service API request.
		"""
	#

	def _check(self):
	#
		"""
Executes checks if the field value is valid.

:return: (bool) True if all checks are passed
:since:  v0.1.00
		"""

		_return = AbstractField._check(self)
		if (_return): _return = self._check_entries_size()

		return _return
	#

	def _check_entries_size(self):
	#
		"""
Checks if the field value has the expected number of entries.

:return: (bool) True if all checks are passed
:since:  v0.1.00
		"""

		error_data = None
		entries_size = (0 if (self.value is None) else len(self.value))

		if (self.required and entries_size < 1): error_data = "required_element"
		elif (self.limit_min is not None
		      and (self.required or entries_size > 0)
		      and self.limit_min > entries_size
		     ): error_data = ( "limit_min", str(self.limit_min) )
		elif (self.limit_max is not None and self.limit_max < entries_size): error_data = ( "limit_max", str(self.limit_max) )

		if (error_data is not None): self.error_data = error_data
		return (error_data is None)
	#

	def _get_dynamic_service_api_query(self):
	#
		"""
Returns the query string used to retrieve the dynamic service field content.

:return: (str) Query string
:since:  v0.1.00
		"""

		query_string_parameters = self.dynamic_api_service_parameters

		query_string_parameters['a'] = "get"
		query_string_parameters['dsd']['oform_id'] = self.form_id
		query_string_parameters['dsd']['oform_field_id'] = self.get_id()
		query_string_parameters['dsd']['oform_field_name'] = self.get_name()
		query_string_parameters['dsd']['oform_field_required'] = ("1" if (self.is_required()) else "0")

		return Link().build_url(Link.TYPE_QUERY_STRING, query_string_parameters)
	#

	def _get_render_context(self):
	#
		"""
Returns the context used for rendering the given field.

:return: (dict) Renderer context
:since:  v0.1.00
		"""

		css_class = ""

		if (self.size == DynamicField.SIZE_MEDIUM): css_class = "pageform_dynamic_form_field_area_medium"
		elif (self.size == DynamicField.SIZE_SMALL): css_class = "pageform_dynamic_form_field_area_small"

		return { "id": "pas_{0}".format(Formatting.escape(self.get_id())),
		         "name": Formatting.escape(self.name),
		         "title": Formatting.escape(self.get_title()),
		         "service_api_query": self._get_dynamic_service_api_query(),
		         "required": self.required,
		         "css_class": css_class,
		         "error_message": ("" if (self.error_data is None) else Formatting.escape(self.get_error_message()))
		       }
	#

	def get_type(self):
	#
		"""
Returns the field type.

:return: (str) Field type
:since:  v0.1.00
		"""

		return "dynamic"
	#

	def render(self):
	#
		"""
Renders the given field.

:return: (str) Valid XHTML form field definition
:since:  v0.1.00
		"""

		return self._render_oset_file("dynamic_form/field", self._get_render_context())
	#

	def set_dynamic_api_service(self, api_service, **kwargs):
	#
		"""
Sets the API service used to for more complex input use cases.

:param api_service: API service name

:since: v0.1.00
		"""

		self.dynamic_api_service = api_service

		self.dynamic_api_service_parameters = { "m": "output",
		                                        "s": "form_api dynamic {0}".format(api_service.replace(".", " ")),
		                                        "dsd": kwargs
		                                      }
	#

	def _set_form_value(self, form):
	#
		"""
Sets the field value based on the given form.

:param form: Form

:since: v0.1.00
		"""

		if (self.dynamic_api_service is not None and self.value is None):
		#
			if (not form.is_supported("form_store")): raise ValueException("The API service can only be used with a form store.")

			form_store_dict = form.get_form_store().get_value_dict()
			self.set_value(form_store_dict.get("form_api_dynamic_{0}".format(self.id), [ ]))
		#

		AbstractField._set_form_value(self, form)
	#
#

##j## EOF