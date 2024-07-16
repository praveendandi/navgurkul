import frappe
import calendar
import erpnext
from frappe import db
from datetime import date
from datetime import datetime ,timedelta
from frappe.exceptions import ValidationError
from frappe.model.document import Document
from frappe import _

import sys
import traceback
import json
from collections import defaultdict
import calendar
# from frappe.utils import datetime, now


@frappe.whitelist()
def get_range_of_date(month):

	if month:
		month = month
		month_num = list(calendar.month_abbr).index(month)
		current_year = datetime.now().year

		num_days = calendar.monthrange(current_year, month_num)[1]
		start_date = datetime(current_year, month_num, 1)
		end_date = datetime(current_year, month_num, num_days)

		all_dates = []

		while start_date <= end_date:
			all_dates.append(start_date.strftime("%Y-%m-%d"))
			start_date += timedelta(days=1)

		return all_dates
	

@frappe.whitelist()
def maping_leave_dates(name,employee,month):

	month_num = list(calendar.month_abbr).index(month)
	current_year = datetime.now().year

	num_days = calendar.monthrange(current_year, month_num)[1]
	start_date = datetime(current_year, month_num, 1)
	end_date = datetime(current_year, month_num, num_days)

	on_leave_data = frappe.db.get_list("Attendance",filters={"docstatus":1,"employee":employee,"status":"On Leave","attendance_date":["Between",[start_date,end_date]]},fields=['attendance_date','status','leave_type'])

	leave_update = frappe.get_doc("Time Tracker",{"name":name,"employee":employee})
	holiday_list = get_employee_holidays(employee)

	if len(on_leave_data)<=0:
		for each in leave_update.time_sheets:
			if each.get("date") in holiday_list:
				frappe.db.set_value("Daily TimeSheet",{"name":each.get("name"),"parent":leave_update.name},{"activity":f'Holiday'})

	for each_leav in on_leave_data:
		row_date = leave_update.time_sheets
		for each in row_date:

			if each_leav.get("attendance_date") == each.get("date"):
				frappe.db.set_value("Daily TimeSheet",{"name":each.get("name"),"parent":leave_update.name},{"activity":f'{each_leav.get("status")}-{ each_leav.get("leave_type")}'})

			if each.get("date") in holiday_list and each.get("hours") <= 0:
				frappe.db.set_value("Daily TimeSheet",{"name":each.get("name"),"parent":leave_update.name},{"activity":f'Holiday'})

			if  each.get("activity"):
				if  "On Leave" in each.get("activity") and not each_leav.get("attendance_date") == each.get("date"):
					
					frappe.db.set_value("Daily TimeSheet",{"name":each.get("name"),"parent":leave_update.name},{"activity":None})
	else:
		frappe.db.commit()
		return {"success":True,"data":"Leave is Update"}
		
def get_employee_holidays(employee_id):

	holiday_list_name = frappe.db.get_value("Employee", employee_id, "holiday_list")

	if holiday_list_name:
		holiday_list = frappe.get_doc("Holiday List", holiday_list_name)
		return [holiday.get("holiday_date") for holiday in holiday_list.holidays]
	
	return []

def total_hours_count(doc, method=None):
	try:
		# Calculate total hours for the current document
		total_hours = 0

		# Get all timesheets for this document
		timesheet_hrs = db.sql("SELECT SUM(hours) FROM `tabDaily TimeSheet` WHERE `parent` = %s", doc.name)
		timesheet_hours = timesheet_hrs[0][0] if timesheet_hrs else 0
		total_hours += timesheet_hours

		# Update the total_hours field in the document
		db.set_value("Time Tracker", {"name": doc.name}, "total_hours", total_hours)
		doc.reload()
	except Exception as e:
		print("An error occurred:", e)


def create_attendance_throgh_timesheet(doc, method=None):
	print("/////////////////////////////")
	if method != "on_submit" and doc.workflow_state != "Approve":
		return

	total_hours_per_date = defaultdict(int)
	month = doc.month
	employee = doc.employee
	month_num = list(calendar.month_abbr).index(month)
	current_year = datetime.now().year

	num_days = calendar.monthrange(current_year, month_num)[1]
	start_date = datetime(current_year, month_num, 1)
	end_date = datetime(current_year, month_num, num_days)

	employee_holidays = get_employee_holidays(employee)
	
	# Time Tracker Date
	for time_sheet in doc.time_sheets:
		date_str = time_sheet.date
		total_hours_per_date[date_str] += time_sheet.hours
		print(total_hours_per_date,";;;;;;;;;;;;;;;;;")
	
		
	# current_date = start_date  # start date of month
	create_attendance_records(employee, total_hours_per_date, employee_holidays)


def create_attendance_records(employee, total_hours_per_date, employee_holidays):
	for date, total_hours in total_hours_per_date.items():
		if not frappe.db.exists("Attendance", {"employee": employee, "attendance_date": date}):
			try:
					attendance_record = frappe.get_doc({
						"doctype": "Attendance",
						"employee": employee,
						"attendance_date": date,
						"docstatus": 1
					})

					if total_hours > 4:
						print(total_hours,type(total_hours),"Greaterthan 4 hours")
						attendance_record.status = "Present"
					elif date not in employee_holidays and 0 < total_hours <= 4:
						print(total_hours,type(total_hours),"less then 4 hours")
						attendance_record.status ="Half Day"
					else:
						if date not in employee_holidays:
							print(date,"/////////////")
							print(total_hours, "0 hours")
							attendance_record.status ="Absent"

					if attendance_record.status:		
						attendance_record.insert()

			except Exception as e:
				frappe.log_error(f"Error creating attendance record for {date}: {e}")

