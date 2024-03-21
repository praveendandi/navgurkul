app_name = "navgurukul_app"
app_title = "Navgurukul"
app_publisher = "nithinreddy"
app_description = "navgurukul hr"
app_email = "nithinreddy@caratred.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/navgurukul_app/css/navgurukul_app.css"
# app_include_js = "/assets/navgurukul_app/js/navgurukul_app.js"

# include js, css files in header of web template
# web_include_css = "/assets/navgurukul_app/css/navgurukul_app.css"
# web_include_js = "/assets/navgurukul_app/js/navgurukul_app.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "navgurukul_app/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "navgurukul_app/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }
fixtures = [
    {
        "dt":
            "Custom Field",
            "filters":[[
                "name",
                "in",
                {
                    "Employee-custom_father_name",
                    "Employee-custom_reporting_manager_name",
                    "Employee-custom_current_experience",
                    "Employee-custom_age",
                    "Employee-custom_joining_department",
                    "Employee-custom_joining_designation",
                    "Employee-custom_employee_assets",
                    "Employee-custom_tshirt",
                    "Employee-custom_laptop",
                    "Employee-custom_comments",
                    "Employee-custom_column_break_euadp",
                    "Employee-custom_mobile_and_sim_card",
                    "Employee-custom_comments_for_moblie_and_sim",
                    "Employee-custom_sim_card",
                    "Employee-custom_comment_for_sim",
                    "Leave Application-custom_reason_for_cancel",
                },
             ]]
    }
]
# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "navgurukul_app.utils.jinja_methods",
# 	"filters": "navgurukul_app.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "navgurukul_app.install.before_install"
# after_install = "navgurukul_app.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "navgurukul_app.uninstall.before_uninstall"
# after_uninstall = "navgurukul_app.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "navgurukul_app.utils.before_app_install"
# after_app_install = "navgurukul_app.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "navgurukul_app.utils.before_app_uninstall"
# after_app_uninstall = "navgurukul_app.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "navgurukul_app.notifications.get_notification_config"

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

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
#     "Employee":"navgurukul_app.navgurukul.events.Employee_2"
        "Leave Application":"navgurukul_app.navgurukul.events.LeaveApplication2"
# 	# "ToDo": "custom_app.overrides.CustomToDo"
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Time Tracker":{
    "on_update": ["navgurukul_app.navgurukul.events.total_hours_count",
                "navgurukul_app.navgurukul.events.month_dates"]
    },
   
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
# 	"all": [
# 		"navgurukul_app.tasks.all"
# 	],
	"daily": [
		"navgurukul_app.navgurukul.events.employee_age_current_experience"
	],
# # 	"hourly": [
# 		"navgurukul_app.tasks.hourly"
# 	],
# 	"weekly": [
# 		"navgurukul_app.tasks.weekly"
# 	],
# 	"monthly": [
# 		"navgurukul_app.tasks.monthly"
# 	],
}

# Testing
# -------

# before_tests = "navgurukul_app.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "navgurukul_app.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "navgurukul_app.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["navgurukul_app.utils.before_request"]
# after_request = ["navgurukul_app.utils.after_request"]

# Job Events
# ----------
# before_job = ["navgurukul_app.utils.before_job"]
# after_job = ["navgurukul_app.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"navgurukul_app.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

