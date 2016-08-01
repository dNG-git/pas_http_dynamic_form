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

from .abstract_select_field import AbstractSelectField
from .dynamic_choices_mixin import DynamicChoicesMixin

class DynamicSelectField(DynamicChoicesMixin, AbstractSelectField):
#
	"""
"DynamicSelectField" provides a selectbox with choices being provided by
an external API service.

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
Constructor __init__(DynamicSelectField)

:param name: Form field name

:since: v0.1.00
		"""

		AbstractSelectField.__init__(self, name)
		DynamicChoicesMixin.__init__(self)
	#

	def _check(self):
	#
		"""
Executes checks if the field value is valid.

:return: (bool) True if all checks are passed
:since:  v0.1.00
		"""

		_return = AbstractSelectField._check(self)
		if (_return): _return = self._check_values_selected_size(1)

		return _return
	#

	def _get_render_context(self):
	#
		"""
Returns the context used for rendering the given field.

:return: (dict) Renderer context
:since:  v0.1.00
		"""

		_return = AbstractSelectField._get_render_context(self)
		_return['service_api_query'] = self._get_choices_service_api_query()

		return _return
	#

	def render(self):
	#
		"""
Renders the given field.

:return: (str) Valid XHTML form field definition
:since:  v0.1.00
		"""

		return self._render_oset_file("dynamic_form/select", self._get_render_context())
	#

	def _set_form(self, form):
	#
		"""
Sets the form this field is part of.

:param form: Form

:since: v0.1.00
		"""

		AbstractSelectField._set_form(self, form)
		DynamicChoicesMixin._set_form(self, form)
	#
#

##j## EOF