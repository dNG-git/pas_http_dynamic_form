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

from dNG.data.xhtml.link import Link
from dNG.runtime.value_exception import ValueException

from .choices_mixin import ChoicesMixin

class DynamicChoicesMixin(ChoicesMixin):
#
	"""
"ChoicesMixin" provides methods to handle selectable options.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: dynamic_form
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
	"""

	def __init__(self):
	#
		"""
Constructor __init__(ChoicesMixin)

:since: v0.1.00
		"""

		ChoicesMixin.__init__(self)

		self.choices_api_service_parameters = None
		"""
Additional parameters transmitted to receive choices by the API service.
		"""
	#

	def _get_choices_service_api_query(self):
	#
		"""
Returns the link to the dynamic form choices API endpoint.

:return: (str) Link to the dynamic form choices API endpoint
:since:  v0.1.00
		"""

		query_string_parameters = self.choices_api_service_parameters

		query_string_parameters['dsd']['oform_id'] = self.form_id
		query_string_parameters['dsd']['oform_field_id'] = self.get_id()
		query_string_parameters['dsd']['oform_field_name'] = self.get_name()

		return Link().build_url(Link.TYPE_QUERY_STRING, query_string_parameters)
	#

	def set_choices_api_service(self, api_service, **kwargs):
	#
		"""
Sets the API service used to provide available choices after the initial
page has been rendered by the client.

:param api_service: API service name

:since: v0.1.00
		"""

		self.choices_api_service_parameters = { "m": "output",
		                                        "s": "form_api choices {0}".format(api_service.replace(".", " ")),
		                                        "a": "get",
		                                        "dsd": kwargs
		                                      }
	#

	def _set_form(self, form):
	#
		"""
Sets the form this field is part of.

:param form: Form

:since: v0.1.00
		"""

		if (self.choices_api_service_parameters is not None):
		#
			if (not form.is_supported("form_store")): raise ValueException("The API service can only be used with a form store.")

			form_store_dict = form.get_form_store().get_value_dict()
			self.choices = (form_store_dict.get("form_api_choices_{0}".format(self.id), [ ]))
		#

		ChoicesMixin._set_form(self, form)
	#
#

##j## EOF