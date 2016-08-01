//j// BOF

/*
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
#echo(pasHttpDynamicFormElementVersion)#
#echo(__FILEPATH__)#
*/

/**
 * @module DynamicFormElement
 */
define([ 'jquery',
         'djt/NodePosition.min',
         'djt/XHtml5FormElement.min',
         'pas/HttpJsonApiDomEditor.min',
         'pas/ExecutingSpinner.min'
       ],
function($, NodePosition, _super, HttpJsonApiDomEditor, ExecutingSpinner) {
	/**
	 * "DynamicFormElement" queries a service API to receive additional data for form
	 * fields.
	 *
	 * @class DynamicFormElement
	 *
	 * @param {object} args Arguments to initialize a given DynamicFormElement
	 */
	function DynamicFormElement(args) {
		if ('service_api_query' in args) {
			if ('type' in args && args.type == 'dynamic') {
				args['init_default_behaviour'] = false;
			}

			_super.call(this, args);
		}

		this.executing_spinner = null;
		this.service_api_query = null;

		if ('service_api_query' in args) {
			this.executing_spinner = new ExecutingSpinner({ id: args.id });
			this.service_api_query = args.service_api_query;

			this._execute_api_query();
		}
	}

	$.extend(DynamicFormElement.prototype, _super.prototype);

	/**
	 * Executes the predefined API query for the dynamic form element.
	 *
	 * @method
	 */
	DynamicFormElement.prototype._execute_api_query = function() {
		if (this.executing_spinner != null) {
			this.executing_spinner.show();
		}

		var hjapi_dom_editor = new HttpJsonApiDomEditor({ id: this.id });
		var hjapi_promise = hjapi_dom_editor.execute({ query: this.service_api_query });

		var _this = this;

		hjapi_promise.always(function() {
			if (_this.executing_spinner != null) {
				_this.executing_spinner.destroy();
			}
		});

		if ($.inArray(this.type, [ 'multiselect', 'select' ]) > -1) {
			hjapi_promise.done(function(data) {
				if ('is_list_complete' in data.response && (!(data.response.is_list_complete))) {
					_this._execute_api_query();
				}
			});
		}
	}

	return DynamicFormElement;
});

//j// EOF