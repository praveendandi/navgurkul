# Copyright (c) 2024, nithinreddy and contributors
# For license information, please see license.txt

# import frappe

 

from datetime import date
from datetime import datetime
import frappe

def execute(filters=None):
	try:
		leave_types = get_leave_types_for_employee(filters)
		columns = get_columns(leave_types)
		data, leave_type = leave_balance(filters)
		chart = get_chart(data, leave_type)

		return columns, data, None, chart
	except Exception as e:
		frappe.log_error(str(e) + " Attendance Regularized")

def get_columns(leave_types):
	columns = [
		{
			"label": ("Employee Number"),
			"fieldtype": "link",
			"fieldname": "employee",
			"options": "Employee",
			"width": 150,
		},
		{
			"label": ("Employee Name"),
			"fieldtype": "data",
			"fieldname": "employee_name",
			"width": 150,
		},
		{
			"label": ("Leave Type"),
			"fieldtype": "Select",
			"fieldname": "leave_type",
			"options": leave_types,
			"width": 150,
		},
		{
			"label": ("Leaves Allocated"),
			"fieldtype": "Float",
			"fieldname": "Leaves Allocated",
			"width": 150,
		},
		{
			"label": ("Total Used Leaves"),
			"fieldtype": "Float",
			"fieldname": "Total Used Leaves",
			"width": 150,
		},
		{
			"label": ("Available Leaves"),
			"fieldtype": "Float",
			"fieldname": "Available Leaves",
			"width": 150,
		},
	]

	return columns

def get_leave_types_for_employee(filters):
	try:
		leave_allocation_list = frappe.db.get_list("Leave Allocation", {
			"employee": filters.get("employee"),
			"docstatus": 1
		}, ["leave_type"])

		leave_types = [d.get('leave_type') for d in leave_allocation_list]
		
		return leave_types
	except Exception as e:
		frappe.log_error(str(e) + " Error getting leave types")


def leave_balance(filters):
    try:
        final_data = []
        allocated_leaves = {}
        total_used_leaves = {}
        
        # Fetch all leave types allocated to the employee if no leave type filter is provided
        if not filters.get("leave_type"):
            leave_allocation_list = frappe.db.get_list("Leave Allocation", {
                "employee": filters.get("employee"),
                "docstatus": 1
            }, ["leave_type"])

            leave_types = set([d.get('leave_type') for d in leave_allocation_list])
        else:
            leave_types = [filters.get("leave_type")]

        # Initialize dictionaries for tracking allocated and used leaves for each leave type
        for leave_type in leave_types:
            allocated_leaves[leave_type] = 0.0
            total_used_leaves[leave_type] = 0.0

        # Fetch leave allocation data
        for leave_type in leave_types:
            leave_allocation_data = frappe.db.get_list("Leave Allocation", {
                "employee": filters.get("employee"),
                "leave_type": leave_type,
                "docstatus": 1
            }, ["new_leaves_allocated"])

            for allocation in leave_allocation_data:
                allocated_leaves[leave_type] += allocation.get("new_leaves_allocated")

        # Fetch leave application data
        leave_application_data = frappe.db.get_list("Leave Application", {
            "employee": filters.get("employee"),
            "leave_type": ("in", leave_types),
            "status": "Approved"
        }, ["employee", "employee_name", "leave_type", "total_leave_days"])

        # Accumulate total used leaves for each leave type
        for application in leave_application_data:
            leave_type = application.get("leave_type")
            total_used_leaves[leave_type] += application.get("total_leave_days")

        # Calculate available leaves for each leave type and construct final data
        for leave_type in leave_types:
            employee = filters.get("employee")
            employee_name = leave_application_data[0].get("employee_name")
            available_leaves = allocated_leaves[leave_type] - total_used_leaves[leave_type]

            # Create data entry for the leave type
            data_entry = {
                "employee": employee,
                "employee_name": employee_name,
                "leave_type": leave_type,
                "Leaves Allocated": allocated_leaves[leave_type],
                "Total Used Leaves": total_used_leaves[leave_type],
                "Available Leaves": available_leaves
            }

            final_data.append(data_entry)

        return final_data, leave_types

    except Exception as e:
        frappe.log_error(str(e) + " Attendance Regularized")

		
def get_chart(final_data, leave_types):
	try:
		# Initialize dictionaries to store data for each leave type
		allocated_leaves = {leave_type: 0 for leave_type in leave_types}
		used_leaves = {leave_type: 0 for leave_type in leave_types}
		available_leaves = {leave_type: 0 for leave_type in leave_types}

		# Aggregate data for each leave type
		for data in final_data:
			leave_type = data['leave_type']
			allocated_leaves[leave_type] += data['Leaves Allocated']
			used_leaves[leave_type] += data['Total Used Leaves']
			available_leaves[leave_type] += data['Available Leaves']

		# Extract leave types and corresponding values for each category
		leave_types = list(leave_types)
		allocated_values = [allocated_leaves[leave_type] for leave_type in leave_types]
		used_values = [used_leaves[leave_type] for leave_type in leave_types]
		available_values = [available_leaves[leave_type] for leave_type in leave_types]

		chart = {
			'data': {
				'labels': leave_types,
				'datasets': [
					{'name': 'Allocated Leaves', 'values': allocated_values, 'chartType': 'bar'},
					{'name': 'Used Leaves', 'values': used_values, 'chartType': 'bar'},
					{'name': 'Available Leaves', 'values': available_values, 'chartType': 'bar'}
				]
			},
			'type': "bar",
			'colors': ['#fa6e0a', '#1127f0', '#3fc53f']
		}

		return chart

	except Exception as e:
		frappe.log_error(str(e) + " Attendance Regularized")

