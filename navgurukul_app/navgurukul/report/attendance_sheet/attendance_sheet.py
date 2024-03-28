# Copyright (c) 2024, nithinreddy and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns = get_columns()
# 	data = get_data()
# 	return columns, data

# def get_columns():
# 	columns = [
# 		{
# 			"label": ("Employee Number"),
# 			"fieldtype": "link",
# 			"fieldname": "employee",
# 			"options": "Employee",
# 			"width": 150,
# 		},
# 		{
# 			"label": ("Employee Name"),
# 			"fieldtype": "data",
# 			"fieldname": "employee_name",
# 			"width": 150,
# 		},
# 		{
# 			"label": ("Leave Type"),
# 			"fieldtype": "Data",
# 			"fieldname": "date",
# 			"width": 150,
# 		},
# 	]
# 	return columns

# def get_data():
# 	# Retrieve employee, employee_name, date, and total_hours
# 	timesheet_data = frappe.db.sql("""
# 		SELECT t.employee, t.employee_name, ts.date, SUM(ts.hours) as total_hours
# 		FROM `tabTime Tracker` as t
# 		LEFT JOIN `tabDaily TimeSheet` as ts ON ts.parent = t.employee
# 		GROUP BY t.employee, ts.date
# 	""", as_dict=1)
# 	print(timesheet_data)
# 	return timesheet_data

# import frappe
# from datetime import datetime, timedelta
# import calendar


# def execute(filters=None):
#     columns, data = get_columns(), get_data()
#     return columns, data
# # def execute(filters=None):
# #     # Gather month and year from filters or use default values
# #     if filters and "month" in filters:
# #         month = int(filters["month"])
# #     else:
# #         month = datetime.now().month
	
# #     if filters and "year" in filters:
# #         year = int(filters["year"])
# #     else:
# #         year = datetime.now().year

# #     # Retrieve columns and data using the specified month and year
# #     columns, data = get_columns(), get_data(month, year)

# #     return columns, data



# def get_columns():
#     # Retrieve distinct dates from the child table
#     distinct_dates = frappe.db.sql("""
#         SELECT DISTINCT date
#         FROM `tabDaily TimeSheet`
#     """, as_dict=True)
	
#     columns = [
#         {
#             "label": "Employee Number",
#             "fieldtype": "Link",
#             "fieldname": "employee",
#             "options": "Employee",
#             "width": 150,
#         },
#         {
#             "label": "Employee Name",
#             "fieldtype": "Data",
#             "fieldname": "employee_name",
#             "width": 150,
#         }
#     ]

#     # Add columns for each date
#     for date in distinct_dates:
#         columns.append({
#             "label": date['date'],
#             "fieldtype": "Select",
#             "fieldname": date['date'],
#             "default":"Present",
#             "width": 150
#         })
#     columns.append({
#         "label": "Total Hours",
# 		"fieldtype": "data",
# 		"fieldname": "total_hours",
# 		"width": 150
# 	})

#     return columns
# def get_data():
#     # Retrieve employee data
#     employees = frappe.db.sql("""
#         SELECT employee, employee_name,total_hours
#         FROM `tabTime Tracker`
#     """, as_dict=True)

#     data = []

#     # Iterate over employees
#     for employee in employees:
#         employee_data = {
#             "employee": employee["employee"],
#             "employee_name": employee["employee_name"],
#             "total_hours":employee["total_hours"]
#         }

#         # Retrieve distinct dates for the employee
#         distinct_dates = frappe.db.sql("""
#             SELECT DISTINCT date
#             FROM `tabDaily TimeSheet`
#             WHERE parent = %s
#         """, employee["employee"], as_dict=True)

#         # Iterate over distinct dates
#         for date in distinct_dates:
#             # Check if there are any records for the employee on the current date
#             present = frappe.db.exists("tabDaily TimeSheet", {"parent": employee["employee"], "date": date['date']})

#             # Add "Present" if there are records, otherwise leave the cell empty
#             employee_data[date['date']] = "Present" if present else ""

#         data.append(employee_data)
# 	# leave_data = frappe.db.sql(""" SELECT `Leave Application`
# 	# 			""")
#     return data


# import frappe
# from datetime import datetime, timedelta
# import calendar


# def execute(filters=None):
# 	columns, data = get_columns(), get_data()
# 	return columns, data


# def get_columns():
# 	# Retrieve distinct dates from the child table
# 	distinct_dates = frappe.db.sql("""
# 		SELECT DISTINCT date
# 		FROM `tabDaily TimeSheet`
# 	""", as_dict=True)

# 	columns = [
# 		{
# 			"label": "Employee Number",
# 			"fieldtype": "Link",
# 			"fieldname": "employee",
# 			"options": "Employee",
# 			"width": 150,
# 		},
# 		{
# 			"label": "Employee Name",
# 			"fieldtype": "Data",
# 			"fieldname": "employee_name",
# 			"width": 150,
# 		}
# 	]

# 	# Add columns for each date
# 	for date in distinct_dates:
# 		columns.append({
# 			"label": date['date'],
# 			"fieldtype": "Select",
# 			"fieldname": date['date'],
# 			"default": "Present",
# 			"width": 150
# 		})

# 	# Add Leave Date column
# 	columns.append({
# 		"label": "Leave Date",
# 		"fieldtype": "Date",
# 		"fieldname": "leave_date",
# 		"width": 150
# 	})

# 	columns.append({
# 		"label": "Total Hours",
# 		"fieldtype": "data",
# 		"fieldname": "total_hours",
# 		"width": 150
# 	})

# 	return columns

# def get_data():
#     # Retrieve employee data
#     employees = frappe.db.sql("""
#         SELECT employee, employee_name,total_hours
#         FROM `tabTime Tracker`
#     """, as_dict=True)

#     data = []

#     # Iterate over employees
#     for employee in employees:
#         employee_data = {
#             "employee": employee["employee"],
#             "employee_name": employee["employee_name"],
#             "total_hours": employee["total_hours"]
#         }

#         # Retrieve distinct dates for the employee
#         distinct_dates = frappe.db.sql("""
#             SELECT DISTINCT date
#             FROM `tabDaily TimeSheet`
#             WHERE parent = %s
#         """, employee["employee"], as_dict=True)

#         # Iterate over distinct dates
#         for date in distinct_dates:
#             # Check if there are any records for the employee on the current date
#             present = frappe.db.exists("tabDaily TimeSheet", {"parent": employee["employee"], "date": date['date']})

#             # Add "Present" if there are records, otherwise leave the cell empty
#             employee_data[date['date']] = "Present" if present else ""

#         # Retrieve leave dates for the employee
#         leave_dates = frappe.db.sql("""
#             SELECT from_date,to_date
#             FROM `tabLeave Application`
#             WHERE employee = %s
#         """, employee["employee"], as_dict=True)

#         # Convert leave dates to strings and store them in the employee data
#         employee_data["from_date"] = ", ".join(str(date["from_date"]) for date in leave_dates)

#         # Append employee_data to data list
#         data.append(employee_data)

#     return data

# import frappe

# def execute(filters=None):
#     columns, data = get_columns(), get_data()
#     return columns, data

# def get_columns():
#     # Retrieve distinct dates from the child table of "Daily Time Sheet"
#     distinct_dates_daily_timesheet = frappe.db.sql("""
#         SELECT DISTINCT date
#         FROM `tabDaily TimeSheet`
#     """, as_dict=True)

#     # Retrieve distinct dates from the "Time Tracker" doctype
#     distinct_dates_time_tracker = frappe.db.sql("""
#         SELECT DISTINCT date
#         FROM `tabTime Tracker`
#     """, as_dict=True)

#     # Retrieve distinct leave dates from the "Leave Application" table
#     distinct_leave_dates = frappe.db.sql("""
#         SELECT DISTINCT from_date
#         FROM `tabLeave Application`
#     """, as_dict=True)

#     # Combine all sets of dates
#     all_dates = set([date['date'] for date in distinct_dates_daily_timesheet] + 
#                     [date['date'] for date in distinct_dates_time_tracker] + 
#                     [date['from_date'] for date in distinct_leave_dates])

#     columns = [
#         {
#             "label": "Employee Number",
#             "fieldtype": "Link",
#             "fieldname": "employee",
#             "options": "Employee",
#             "width": 150,
#         },
#         {
#             "label": "Employee Name",
#             "fieldtype": "Data",
#             "fieldname": "employee_name",
#             "width": 150,
#         }
#     ]

#     # Add columns for each date from all sets
#     for date in all_dates:
#         columns.append({
#             "label": str(date),  # Convert to string if not already
#             "fieldtype": "Select",
#             "fieldname": str(date),  # Convert to string if not already
#             "default": "Present",
#             "width": 150
#         })

#     return columns

# def get_data():
#     # Retrieve employee data
#     employees = frappe.db.sql("""
#         SELECT employee, employee_name
#         FROM `tabEmployee`
#     """, as_dict=True)

#     data = []

#     # Iterate over employees
#     for employee in employees:
#         employee_data = {
#             "employee": employee["employee"],
#             "employee_name": employee["employee_name"]
#         }

#         # Retrieve distinct dates for the employee from the "Daily Time Sheet" doctype
#         distinct_dates_daily_timesheet = frappe.db.sql("""
#             SELECT DISTINCT date
#             FROM `tabDaily TimeSheet`
#             WHERE parent = %s
#         """, employee["employee"], as_dict=True)

#         # Retrieve distinct dates for the employee from the "Time Tracker" doctype
#         distinct_dates_time_tracker = frappe.db.sql("""
#             SELECT DISTINCT date
#             FROM `tabTime Tracker`
#             WHERE employee = %s
#         """, employee["employee"], as_dict=True)

#         # Retrieve distinct leave dates for the employee from the "Leave Application" table
#         distinct_leave_dates = frappe.db.sql("""
#             SELECT DISTINCT from_date
#             FROM `tabLeave Application`
#             WHERE employee = %s
#         """, employee["employee"], as_dict=True)

#         # Combine all sets of dates
#         all_dates = set([date['date'] for date in distinct_dates_daily_timesheet] + 
#                         [date['date'] for date in distinct_dates_time_tracker] + 
#                         [date['from_date'] for date in distinct_leave_dates])

#         # Iterate over all dates
#         for date in all_dates:
#             # Check if the date is present in the "Daily Time Sheet" child table
#             present_daily_timesheet = frappe.db.exists("tabDaily TimeSheet", {"parent": employee["employee"], "date": date})

#             # Check if the date is present in the "Time Tracker" doctype
#             present_time_tracker = frappe.db.exists("tabTime Tracker", {"employee": employee["employee"], "date": date})

#             # Check if the date is a leave date
#             leave_date = frappe.db.exists("tabLeave Application", {"employee": employee["employee"], "from_date": date})

#             # Set the status based on the presence in the child table, "Time Tracker" doctype, and leave application
#             if present_daily_timesheet:
#                 status = "Present"
#             elif present_time_tracker:
#                 status = "Present"
#             elif leave_date:
#                 status = "Leave"
#             else:
#                 status = ""

#             employee_data[str(date)] = status

#         data.append(employee_data)

#     return data

# import frappe

# def execute(filters=None):
#     columns, data = get_columns(), get_data()
#     return columns, data

# def get_columns():
#     # Retrieve distinct dates from the child table "tabDaily TimeSheet"
#     distinct_dates_daily_timesheet = frappe.db.sql("""
#         SELECT DISTINCT date
#         FROM `tabDaily TimeSheet`
#     """, as_dict=True)

#     # Retrieve distinct leave dates from the "Leave Application" table
#     distinct_leave_dates = frappe.db.sql("""
#         SELECT DISTINCT from_date
#         FROM `tabLeave Application`
#     """, as_dict=True)

#     # Combine all sets of dates
#     all_dates = set([date['date'] for date in distinct_dates_daily_timesheet] + 
#                     [date['from_date'] for date in distinct_leave_dates])

#     columns = [
#         {
#             "label": "Employee Number",
#             "fieldtype": "Link",
#             "fieldname": "employee",
#             "options": "Employee",
#             "width": 150,
#         },
#         {
#             "label": "Employee Name",
#             "fieldtype": "Data",
#             "fieldname": "employee_name",
#             "width": 150,
#         }
#     ]

#     # Add columns for each date from both sets
#     for date in all_dates:
#         columns.append({
#             "label": str(date),  # Convert to string if not already
#             "fieldtype": "Select",
#             "fieldname": str(date),  # Convert to string if not already
#             "default": "Present",
#             "width": 150
#         })

#     return columns

# def get_data():
#     # Retrieve distinct dates from the child table "tabDaily TimeSheet"
#     distinct_dates_daily_timesheet = frappe.db.sql("""
#         SELECT DISTINCT date
#         FROM `tabDaily TimeSheet`
#     """, as_dict=True)

#     # Retrieve distinct leave dates from the "Leave Application" table
#     distinct_leave_dates = frappe.db.sql("""
#         SELECT DISTINCT from_date
#         FROM `tabLeave Application`
#     """, as_dict=True)

#     # Combine all sets of dates
#     all_dates = set([date['date'] for date in distinct_dates_daily_timesheet] + 
#                     [date['from_date'] for date in distinct_leave_dates])

#     data = []

#     # Retrieve all employees from the "Time Tracker" doctype
#     employees = frappe.db.sql("""
#         SELECT employee, employee_name
#         FROM `tabTime Tracker`
#     """, as_dict=True)

#     # Iterate over employees
#     for employee in employees:
#         employee_data = {
#             "employee": employee["employee"],
#             "employee_name": employee["employee_name"]
#         }

#         # Retrieve distinct dates for the employee from the child table "tabDaily TimeSheet"
#         distinct_dates_daily_timesheet = frappe.db.sql("""
#             SELECT DISTINCT date
#             FROM `tabDaily TimeSheet`
#             WHERE parent = %s
#         """, employee["employee"], as_dict=True)

#         # Retrieve distinct leave dates for the employee from the "Leave Application" table
#         distinct_leave_dates = frappe.db.sql("""
#             SELECT DISTINCT from_date
#             FROM `tabLeave Application`
#             WHERE employee = %s
#         """, employee["employee"], as_dict=True)

#         # Combine both sets of dates
#         all_dates = set([date['date'] for date in distinct_dates_daily_timesheet] + 
#                         [date['from_date'] for date in distinct_leave_dates])

#         # Iterate over all dates
#         for date in all_dates:
#             # Check if the date is present in the child table "tabDaily TimeSheet"
#             present_daily_timesheet = frappe.db.exists("tabDaily TimeSheet", {"parent": employee["employee"], "date": date})

#             # Check if the date is a leave date
#             leave_date = frappe.db.exists("tabLeave Application", {"employee": employee["employee"], "from_date": date})

#             # Set the status based on the presence in the child table and leave application
#             if present_daily_timesheet:
#                 status = "Present"
#             elif leave_date:
#                 status = "Leave"
#             else:
#                 status = ""

#             employee_data[str(date)] = status

#         data.append(employee_data)

#     return data
# import frappe

# def execute(filters=None):
#     columns, data = get_columns(), get_data()
#     return columns, data

# def get_columns():
#     # Retrieve distinct dates from the child table "tabDaily TimeSheet"
#     distinct_dates_daily_timesheet = frappe.db.sql("""
#         SELECT DISTINCT date
#         FROM `tabDaily TimeSheet`
#         ORDER BY date
#     """, as_dict=True)

#     # Retrieve distinct leave dates from the "Leave Application" table
#     distinct_leave_dates = frappe.db.sql("""
#         SELECT DISTINCT from_date
#         FROM `tabLeave Application`
#         ORDER BY from_date
#     """, as_dict=True)

#     # Combine all sets of dates
#     all_dates = sorted([date['date'] for date in distinct_dates_daily_timesheet] + 
#                        [date['from_date'] for date in distinct_leave_dates])

#     columns = [
#         {
#             "label": "Employee Number",
#             "fieldtype": "Link",
#             "fieldname": "employee",
#             "options": "Employee",
#             "width": 150,
#         },
#         {
#             "label": "Employee Name",
#             "fieldtype": "Data",
#             "fieldname": "employee_name",
#             "width": 150,
#         }
#     ]

#     # Add columns for each date from both sets
#     for date in all_dates:
#         columns.append({
#             "label": str(date),  # Convert to string if not already
#             "fieldtype": "Select",
#             "fieldname": str(date),  # Convert to string if not already
#             "default": "Present",  # Default to "Present" status
#             "width": 150
#         })

#     return columns

# def get_data():
#     data = []

#     # Retrieve all employees from the "Time Tracker" doctype
#     employees = frappe.db.sql("""
#         SELECT employee, employee_name
#         FROM `tabTime Tracker`
#     """, as_dict=True)

#     # Iterate over employees
#     for employee in employees:
#         employee_data = {
#             "employee": employee["employee"],
#             "employee_name": employee["employee_name"]
#         }

#         # Retrieve distinct dates for the employee from the child table "tabDaily TimeSheet"
#         distinct_dates_daily_timesheet = frappe.db.sql("""
#             SELECT DISTINCT date
#             FROM `tabDaily TimeSheet`
#             WHERE parent = %s
#             ORDER BY date
#         """, employee["employee"], as_dict=True)

#         # Retrieve distinct leave dates for the employee from the "Leave Application" table
#         distinct_leave_dates = frappe.db.sql("""
#             SELECT DISTINCT from_date
#             FROM `tabLeave Application`
#             WHERE employee = %s
#             ORDER BY from_date
#         """, employee["employee"], as_dict=True)

#         # Combine both sets of dates
#         all_dates = sorted([date['date'] for date in distinct_dates_daily_timesheet] + 
#                            [date['from_date'] for date in distinct_leave_dates])

#         # Iterate over all dates
#         for date in all_dates:
#             # Check if the date is present in the child table "tabDaily TimeSheet"
#             present_daily_timesheet = frappe.db.exists("tabDaily TimeSheet", {"parent": employee["employee"], "date": date})

#             # Check if the date is a leave date
#             leave_date = frappe.db.exists("tabLeave Application", {"employee": employee["employee"], "from_date": date})

#             # Set the status based on the presence in the child table and leave application
#             if present_daily_timesheet:
#                 status = "Present"
#             elif leave_date:
#                 status = "Leave"
#             else:
#                 status = ""

#             employee_data[str(date)] = status

#         data.append(employee_data)

#     return data

import frappe
from datetime import datetime

def execute(filters=None):
    selected_month = filters.get("selected_month")
    columns, data = get_columns(selected_month), get_data(selected_month)
    return columns, data

def get_columns(selected_month):
    # Convert the selected month to a datetime object
    selected_month_date = datetime.strptime(selected_month, "%Y-%m")

    # Retrieve distinct dates from the child table "tabDaily TimeSheet" within the selected month
    distinct_dates_daily_timesheet = frappe.db.sql("""
        SELECT DISTINCT date
        FROM `tabDaily TimeSheet`
        WHERE MONTH(date) = %s AND YEAR(date) = %s
        ORDER BY date ASC
    """, (selected_month_date.month, selected_month_date.year), as_dict=True)

    # Retrieve distinct leave dates from the "Leave Application" table within the selected month
    distinct_leave_dates = frappe.db.sql("""
        SELECT DISTINCT from_date
        FROM `tabLeave Application`
        WHERE MONTH(from_date) = %s AND YEAR(from_date) = %s
        ORDER BY from_date ASC
    """, (selected_month_date.month, selected_month_date.year), as_dict=True)

    # Combine all sets of dates and sort them in ascending order
    all_dates = sorted([date['date'] for date in distinct_dates_daily_timesheet] + 
                       [date['from_date'] for date in distinct_leave_dates])

    columns = [
        {
            "label": "Employee Number",
            "fieldtype": "Link",
            "fieldname": "employee",
            "options": "Employee",
            "width": 150,
        },
        {
            "label": "Employee Name",
            "fieldtype": "Data",
            "fieldname": "employee_name",
            "width": 150,
        }
    ]

    # Add columns for each date from both sets
    for date in all_dates:
        columns.append({
            "label": str(date),  # Convert to string if not already
            "fieldtype": "Select",
            "fieldname": str(date),  # Convert to string if not already
            "default": "Present",  # Default to "Present" status
            "width": 150
        })

    return columns

def get_data(selected_month):
    data = []

    # Convert the selected month to a datetime object
    selected_month_date = datetime.strptime(selected_month, "%Y-%m")

    # Retrieve all employees from the "Time Tracker" doctype
    employees = frappe.db.sql("""
        SELECT employee, employee_name
        FROM `tabTime Tracker`
    """, as_dict=True)

    # Iterate over employees
    for employee in employees:
        employee_data = {
            "employee": employee["employee"],
            "employee_name": employee["employee_name"]
        }

        # Retrieve distinct dates for the employee from the child table "tabDaily TimeSheet" within the selected month
        distinct_dates_daily_timesheet = frappe.db.sql("""
            SELECT DISTINCT date
            FROM `tabDaily TimeSheet`
            WHERE parent = %s AND MONTH(date) = %s AND YEAR(date) = %s
            ORDER BY date ASC
        """, (employee["employee"], selected_month_date.month, selected_month_date.year), as_dict=True)

        # Retrieve distinct leave dates for the employee from the "Leave Application" table within the selected month
        distinct_leave_dates = frappe.db.sql("""
            SELECT DISTINCT from_date
            FROM `tabLeave Application`
            WHERE employee = %s AND MONTH(from_date) = %s AND YEAR(from_date) = %s
            ORDER BY from_date ASC
        """, (employee["employee"], selected_month_date.month, selected_month_date.year), as_dict=True)

        # Combine both sets of dates and sort them in ascending order
        all_dates = sorted([date['date'] for date in distinct_dates_daily_timesheet] + 
                           [date['from_date'] for date in distinct_leave_dates])

        # Iterate over all dates
        for date in all_dates:
            # Check if the date is present in the child table "tabDaily TimeSheet"
            present_daily_timesheet = frappe.db.exists("tabDaily TimeSheet", {"parent": employee["employee"], "date": date})

            # Check if the date is a leave date
            leave_date = frappe.db.exists("tabLeave Application", {"employee": employee["employee"], "from_date": date})

            # Set the status based on the presence in the child table and leave application
            if present_daily_timesheet:
                status = "Present"
            elif leave_date:
                status = "Leave"
            else:
                status = ""

            employee_data[str(date)] = status

        data.append(employee_data)

    return data









