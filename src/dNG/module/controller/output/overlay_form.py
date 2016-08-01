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

from dNG.data.http.translatable_error import TranslatableError
from dNG.data.xhtml.formatting import Formatting as XHtmlFormatting
from dNG.data.xhtml.link import Link
from dNG.module.controller.abstract_http import AbstractHttp as AbstractHttpController
from dNG.runtime.value_exception import ValueException

from .form_parse_mixin import FormParseMixin

class OverlayForm(FormParseMixin, AbstractHttpController):
#
	"""
The "Form" class implements the form view.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: dynamic_form
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
	"""

	def execute_render(self):
	#
		"""
Action for "render"

:since: v0.1.00
		"""

		if (self._is_primary_action()): raise TranslatableError("core_access_denied", 403)

		if ("url_parameters" not in self.context): raise ValueException("URL parameters required for the overlay form are not defined")

		form_content = self._parse_context_form()
		form_id = XHtmlFormatting.escape(self.context['object'].get_form_render_id())

		form_query_string = Link().build_url(Link.TYPE_QUERY_STRING, self.context['url_parameters'])

		form = "<form id=\"pas_{0}\" action=\"\" data-pas-dom-editor-query=\"{1}\">{2}</form>"
		form = form.format(form_id, form_query_string, form_content)

		self.set_action_result(form)
	#
#

##j## EOF