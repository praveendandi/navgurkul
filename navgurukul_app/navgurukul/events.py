# import erpnext


import frappe
import erpnext
import frappe
from frappe import db
from datetime import date
from datetime import datetime ,timedelta
from frappe.exceptions import ValidationError
from frappe.model.document import Document
from frappe import _
from hrms.hr.doctype.leave_application.leave_application import LeaveApplication
from hrms.hr.doctype.leave_application.leave_application import get_leave_balance_on
import sys
import traceback
import json
from collections import defaultdict


class LeaveApplication2(LeaveApplication):
	def validate(self):
		super().validate()


	def after_insert(self):
		self.check_status()

	def on_update(self):
		self.check_status_reject()
			
	def check_status(self):
			
			if self.workflow_state == 'Pending':
				self.validate_before_rejection('Pending')
	def check_status_reject(self):
			if self.workflow_state == 'Reject':
				self.validate_before_rejection('Reject')
			

	def validate_before_rejection(self, action):
		# try:
		if action == "Pending" and not self.custom_reason_for_cancel:
			frappe.msgprint("Heyy😄!! Your leave request has been submitted🤩🏝️!")
			
		if action == 'Reject' and not self.custom_reason_for_cancel:
			frappe.throw("Please provide a reason for rejection before proceeding.")
		if self.workflow_state == "Reject":
			frappe.msgprint(f"🚨 Heyy 👩🏻‍💻!! The Leave has been rejected for {self.employee_name}!! 📣")
				
	
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

def month_dates(doc, method=None):
	try:
		timesheets = frappe.db.sql("""SELECT t.name,t.employee,t.employee_name, t.month,t.workflow_state FROM `tabTime Tracker` as t WHERE 
		t.docstatus = 0 OR t.docstatus = 1""", as_dict=True) 

		# total_hours_per_date = defaultdict(int)
		# Calculate total hours for this employee
		for timesheet in timesheets:
			timesheet_hrs = frappe.db.sql("SELECT ts.date,ts.hours FROM `tabDaily TimeSheet` as ts WHERE `parent` = %s", timesheet.name, as_dict=True)
			total_hours_per_date = {}
			# Convert each date string to datetime object and format month abbreviation
			for entry in timesheet_hrs:
				date_str = entry.get('date')
				total_hours = entry.get('hours', 0)
				if date_str:
					if isinstance(date_str, str):
						date = datetime.strptime(date_str, "%Y-%m-%d")
					else:
						date = datetime(date_str.year, date_str.month, date_str.day)
					if date_str in total_hours_per_date:
						total_hours_per_date[date_str] += total_hours
					else:
						total_hours_per_date[date_str] = total_hours

					for date_str, total_hours in total_hours_per_date.items():
						# print(f"Date: {date_str}, Total Hours: {total_hours}")
						if total_hours > 12:
							raise ValidationError("Hey there!! You cannot enter more than 12 log hours for the same date. Please check!😊")
								 
					# teas_date = date.strftime("%b %Y")
					teas_date = date_str.strftime("%b %Y")

					month = timesheet.month
					current_year = datetime.now().year
					month_year = f"{month} {current_year}"

					if month_year != teas_date:
						raise ValidationError("⚠️ Oops! Month and the date on the Timesheet has a mismatch. Please check. 😊")
					else: 
						pass  
					leave_applications = frappe.get_list("Leave Application", filters={"employee": timesheet.employee, "status": "Approved"}, fields=['from_date', 'to_date', 'leave_type','total_leave_days'])
					for leave_application in leave_applications:
						from_date = leave_application.get('from_date')
						to_date = leave_application.get('to_date')
						# leave_type = leave_application.get('leave_type')
						total_leave_days = leave_application.get('total_leave_days')
						# For full-day leaves, check if the timesheet date falls within the leave period
						# if from_date <= date.date() <= to_date and total_leave_days > 0.5:
						# 	raise ValidationError(f"Heyy there‼️ You cannot access this date as you have applied a leave on {date.date()}. Please check!😇")
						if from_date <= date.date() <= to_date:
							if total_leave_days > 0.5:
								raise ValidationError(f"Hey there! You cannot enter hours for a full-day leave on {date.date()}. Please check!😊")	
						
							if total_leave_days <= 0.5:
								if entry.get('hours') and entry.get('hours') > 4:
									raise ValidationError(f"Hey there! You cannot enter more than 4 hours for a half-day leave on {date.date()}. Please check!😊")
			
		# Display success message once after the loop completes
		if doc.workflow_state == "Pending" and not doc.reason_for_reject:
			frappe.msgprint("🎉 Timesheet has been successfully updated 🚀")
				
		if doc.workflow_state == "Approve":
			frappe.msgprint(f"Heyy 👩🏻‍💻!! The time sheet has been approved for {doc.employee_name}!! 📣")
			
		if doc.workflow_state == "Reject":
			reason_for_reject(doc)
			frappe.msgprint(f"🚨 Heyy 👩🏻‍💻!! The time sheet has been rejected for {doc.employee_name}!! 📣")
				
					
		
	except Exception as e:
		frappe.throw(f"{e}")


from datetime import datetime

def reason_for_reject(doc):
	if doc.workflow_state == "Reject" and not doc.reason_for_reject:
		raise ValidationError("Please provide a reason for rejection before proceeding.")
	
def employee_age_current_experience():
	try:
		emp_data = frappe.get_all("Employee", fields=["name", "date_of_joining", "date_of_birth"])
		for emp in emp_data:
			name = emp.name
			date_of_joining = emp.date_of_joining
			date_of_birth = emp.date_of_birth

			# Calculate experience only if date_of_joining is not None
			if date_of_joining:
				today = date.today()
				# If the joining date is in the future, set current_experience as empty
				if today < date_of_joining:
					current_experience = ""
				else:
					years = today.year - date_of_joining.year
					months = today.month - date_of_joining.month
					if today.day < date_of_joining.day:
						months -= 1
					if months < 0:
						years -= 1
						months += 12
					current_experience = f"{years} Year {months} Months"

				# Set the calculated experience in the 'current_experience' field
				frappe.db.set_value('Employee', name, 'custom_current_experience', current_experience ,update_modified=False)

			# Calculate age based on date_of_birth
			if date_of_birth:
				age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
				frappe.db.set_value('Employee', name, 'custom_age', age ,update_modified=False)
	except Exception as e:
		print("An error occurred:", e)	

@frappe.whitelist()
def get_employee_ctc(name):
	try:
		employee_ctc = frappe.db.get_list("Employee",{"name":name},['employee_name','ctc'])
		return employee_ctc
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		frappe.log_error("line No:{}\n{}".format(exc_tb.tb_lineno, traceback.format_exc()), "get_employee_ctc")


def create_attendance(doc, method=None):
	if method == "on_submit" or doc.workflow_state == "Approve":
		for time_sheet in doc.time_sheets:
			if not frappe.db.exists("Attendance",{"employee":doc.employee,"attendance_date":time_sheet.date}):
				try:
					create_attendance_record = frappe.get_doc({
						"doctype": "Attendance",
						"employee": doc.employee,
						"attendance_date": time_sheet.date,
						"docstatus":1
					})
					if time_sheet.hours > 4:
						create_attendance_record.status = "Present"
						
					else:
						create_attendance_record.status = "Half Day"
						leave_type =create_leave_throw_attendance(doc,time_sheet.date)
						create_attendance_record.leave_type = leave_type
						
				
					create_attendance_record.insert()

				except Exception as e:
					continue


def create_leave_throw_attendance(doc,date):
	try:

		employee = doc.employee
		leave_type = ['Casual Leave','Wellness Leave']
		leave_date = date
		balance = {}

		for i in leave_type:
			balance_leave = get_leave_balance_on(employee,i,leave_date)
			balance.update({i:balance_leave})

		create_leave = frappe.get_doc({
			"doctype": "Leave Application",
			"employee": doc.employee,
			"from_date":date,
			"to_date":date,
			"half_day": 1,
			"docstatus":1

			})
		
		if balance.get("Casual Leave",None):
			create_leave.leave_type = "Casual Leave"
		else:
			create_leave.leave_type = "Wellness Leave"

		create_leave.insert()

		return create_leave.leave_type
	
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		frappe.log_error("line No:{}\n{}".format(exc_tb.tb_lineno, traceback.format_exc()), "create_leave_throw_attendance")


 
 
@frappe.whitelist()
def get_travel_request(doc):
	
	try:
		row_data = json.loads(doc)
		
		costing_child = row_data.get("costings")
		
		travel_details = row_data.get("itinerary")
		
		return costing_child
	
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		frappe.log_error("line No:{}\n{}".format(exc_tb.tb_lineno, traceback.format_exc()), "get_travel_request")

# def weekoff_leave(doc, method=None):
# 	weekoff_leave_data = frappe.db.get_list("Leave Application", 
# 											['employee', 'from_date', 'to_date', 'total_leave_days', 'leave_type'])
	
# 	# Dictionary to hold leave count for each employee
# 	leave_count = {}
	
# 	# Count leaves for each employee
# 	for emp in weekoff_leave_data:
# 		emp_id = emp['employee']
# 		leave_type = emp['leave_type']
		
# 		# Initialize leave count for employee if not already present
# 		if emp_id not in leave_count:
# 			leave_count[emp_id] = 0
		
# 		# If leave type is not "week off", increment leave count
# 		if leave_type == "Week Off":
# 			leave_count[emp_id] += 1
	
# 	# Check if any employee has exceeded the leave limit
# 	for emp_id, count in leave_count.items():
# 		if count > 2:
# 			frappe.throw(f"Employee {emp_id} has exceeded the leave limit for the month.")
# 	print(leave_count)
# 	return leave_count
# def weekoff_leave(doc, method=None):
#     # Get the current month and year
#     current_month = datetime.date.today().month
#     current_year = datetime.date.today().year
    
#     # Get the first and last day of the current month
#     first_day_month = datetime.date(current_year, current_month, 1)
#     last_day_month = datetime.date(current_year, current_month+1, 1) - datetime.timedelta(days=1)
    
#     # Retrieve leave applications for the current month
#     weekoff_leave_data = frappe.db.get_list("Leave Application", 
#                                             filters={'from_date': ['>=', first_day_month],
#                                                      'to_date': ['<=', last_day_month],
#                                                      'leave_type': 'Week Off'},
#                                             fields=['employee', 'from_date'])
#     print(weekoff_leave_data,";;;;;;;;;")
#     # Dictionary to hold leave count for each employee
#     leave_count = defaultdict(int)
    
#     # Count week off leaves for each employee
#     for leave_app in weekoff_leave_data:
#         emp_id = leave_app['employee']
#         leave_count[emp_id] += 1
    
#     # Check if any employee has already taken two week off leaves
#     for emp_id, count in leave_count.items():
#         if count >= 2:
#             frappe.throw(f"Employee {emp_id} has already taken the maximum number of week off leaves for this month.")
