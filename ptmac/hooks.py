# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "ptmac"
app_title = "ptmac"
app_publisher = "jonathan"
app_description = "ptmac"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "jof2jc@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ptmac/css/ptmac.css"
# app_include_js = "/assets/ptmac/js/ptmac.js"

# include js, css files in header of web template
# web_include_css = "/assets/ptmac/css/ptmac.css"
# web_include_js = "/assets/ptmac/js/ptmac.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "ptmac.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "ptmac.install.before_install"
# after_install = "ptmac.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ptmac.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }
doc_events = {
    "Contact": {
	"autoname": "ptmac.ptmac.custom_ptmac.autoname"
    },
    "Item": {
	"autoname": "ptmac.ptmac.custom_ptmac.item_autoname"
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"ptmac.tasks.all"
# 	],
# 	"daily": [
# 		"ptmac.tasks.daily"
# 	],
# 	"hourly": [
# 		"ptmac.tasks.hourly"
# 	],
# 	"weekly": [
# 		"ptmac.tasks.weekly"
# 	]
# 	"monthly": [
# 		"ptmac.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "ptmac.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "ptmac.event.get_events"
# }

