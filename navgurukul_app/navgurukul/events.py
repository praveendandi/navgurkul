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
from hrms.hr.doctype.leave_application.leave_application import get_leave_balance_on
import sys
import traceback
import json
from collections import defaultdict
import calendar
from frappe.utils import datetime, now




def after_insert(self,method=None):
	check_status(self)

def on_submit(self,method=None):
	check_approve(self)


def on_update(self,method=None):
	check_status_reject(self)
		
def check_status(self):
		
	if self.workflow_state == 'Pending':
		validate_before_rejection(self,'Pending')

def check_approve(self):
	if self.workflow_state == 'Approve' and '__unsaved' not in self.as_dict():
		validate_before_rejection(self,'Approve')

def check_status_reject(self):
	if self.workflow_state == 'Reject':
		validate_before_rejection(self,'Reject')
		

def validate_before_rejection(self, action):
	# try:
	if action == "Pending" and not self.custom_reason_for_cancel:
		frappe.msgprint("Heyy😄!! Your leave request has been submitted🤩🏝️!")
	if action == "Approve":
		frappe.msgprint(f"Heyy 👩🏻‍💻!! The Leave has been approved for {self.employee_name}!! 📣")
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
		timesheets = frappe.db.sql("""
			SELECT t.name, t.employee, t.employee_name, t.month, t.workflow_state
			FROM `tabTime Tracker` AS t
			WHERE (t.docstatus = 0 OR t.docstatus = 1) AND t.employee = %s
		""", (doc.employee,), as_dict=True)
		
		for timesheet in timesheets:
			timesheet_hrs = frappe.db.sql("""
				SELECT ts.date, ts.hours 
				FROM `tabDaily TimeSheet` AS ts 
				WHERE `parent` = %s
			""", (timesheet.name,), as_dict=True)
			
			total_hours_per_date = defaultdict(int)
			for entry in timesheet_hrs:
				date_str = entry.get('date')
				hours = entry.get('hours', 0)
				if date_str:
					if isinstance(date_str, str):
						date = datetime.strptime(date_str, "%Y-%m-%d")
					else:
						date = datetime(date_str.year, date_str.month, date_str.day)
					# date = datetime.strftime(date_str, "%Y-%m-%d")
					total_hours_per_date[date] += hours
					if total_hours_per_date[date] > 12:
						raise frappe.ValidationError(_("You cannot enter more than 12 log hours for the same date. Please check! 😊"))

					teas_date = date_str.strftime("%b %Y")

					month = timesheet.month
					current_year = datetime.now().year
					month_year = f"{month} {current_year}"

					if month_year != teas_date:
						raise ValidationError("⚠️ Oops! Month and the date on the Timesheet has a mismatch. Please check. 😊")
				
					validate_leave_overlap(timesheet.employee, date)
		
		total_hours_count(doc)

		display_workflow_message(doc)
		
	except Exception as e:
		frappe.throw(str(e))

def validate_leave_overlap(employee, date):
	leave_applications = frappe.get_list("Leave Application", filters={"employee": employee, "status": "Approved"}, fields=['from_date', 'to_date', 'leave_type', 'total_leave_days'])
	for leave in leave_applications:
		from_date = leave.get('from_date')
		to_date = leave.get('to_date')
		total_leave_days = leave.get('total_leave_days')

		if from_date <= date.date() <= to_date:
			if total_leave_days > 0.5:
				raise frappe.ValidationError(f"Cannot enter hours for a full-day leave on {date}. Please check! 😊")
			elif total_leave_days > 4:
				raise frappe.ValidationError(f"Cannot enter more than 4 hours for a half-day leave on {date}. Please check! 😊")

def display_workflow_message(doc):
	if doc.workflow_state == "Pending" and not doc.reason_for_reject:
		frappe.msgprint(_("Timesheet has been successfully updated 🚀"))
	elif doc.workflow_state == "Approve":
		frappe.msgprint(_("The timesheet has been approved for {0}!! 📣").format(doc.employee_name))
	elif doc.workflow_state == "Reapply" and not doc.reason_for_reject:
		frappe.throw(_("Please provide a reason for reapply before proceeding."))
	elif doc.workflow_state == "Reapply" and doc.reason_for_reject:
		frappe.msgprint(_("The timesheet has been reapply and sent for resubmission - {0}!! 📣").format(doc.employee_name))
	elif doc.workflow_state == "Resubmitted Done":
		frappe.msgprint(_("The timesheet has been Resubmitted Done for {0}!! 📣").format(doc.employee_name))


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
	
	for time_sheet in doc.time_sheets:
		date_str = time_sheet.date.strftime("%Y-%m-%d")
		total_hours_per_date[date_str] += time_sheet.hours
		
	current_date = start_date
	while current_date <= end_date:
		date_str = current_date.strftime("%Y-%m-%d")
		
		if date_str not in total_hours_per_date and date_str not in employee_holidays:
			if not check_existing_leave_application(employee, date_str):
				create_leave_application(employee, date_str)
		
		current_date += timedelta(days=1)

	create_attendance_records(employee, total_hours_per_date, employee_holidays)

def create_leave_application(employee, date_str):
	try:
		leave_application = frappe.get_doc({
			"doctype": "Leave Application",
			"employee": employee,
			"leave_type": "Leave Without Pay",
			"from_date": date_str,
			"to_date": date_str,
			"docstatus": 1,
			"status":"Approved"
		})
		leave_application.insert()
	except Exception as e:
		frappe.log_error(f"Error creating leave application for {date_str}: {e}")

def create_attendance_records(employee, total_hours_per_date, employee_holidays):
	for date, total_hours in total_hours_per_date.items():
		if not frappe.db.exists("Attendance", {"employee": employee, "attendance_date": date}):
			try:
				if not check_existing_leave_application(employee, date):
					attendance_record = frappe.get_doc({
						"doctype": "Attendance",
						"employee": employee,
						"attendance_date": date,
						"docstatus": 1
					})
					if total_hours > 4:
						attendance_record.status = "Present"
					elif date not in employee_holidays:
						attendance_record.status = "Half Day"
						leave_type = create_leave_throw_attendance(employee, date)
						attendance_record.leave_type = leave_type
					else:
						attendance_record.status = "Half Day"
					
					attendance_record.insert()
			except Exception as e:
				frappe.log_error(f"Error creating attendance record for {date}: {e}")

def check_existing_leave_application(employee, date_str):
	leave_exists = frappe.db.exists({
		"doctype": "Leave Application",
		"employee": employee,
		"from_date": ["<=", date_str],
		"to_date": [">=", date_str],
		"status": "Approved"
	})
	if leave_exists:
		frappe.log_error(f"Conflict: Employee {employee} already has approved leave application for {date_str}")
	return leave_exists

def get_employee_holidays(employee_id):
	holiday_list_name = frappe.db.get_value("Employee", employee_id, "holiday_list")
	if holiday_list_name:
		holiday_list = frappe.get_doc("Holiday List", holiday_list_name)
		return [holiday.holiday_date.strftime("%Y-%m-%d") for holiday in holiday_list.holidays]
	return []



def create_leave_throw_attendance(doc,date):
	try:

		employee = doc.employee

		create_leave = frappe.get_doc({
			"doctype": "Leave Application",
			"employee": doc.employee,
			"leave_type":"Leave Without Pay",
			"from_date":date,
			"to_date":date,
			"half_day": 1,
			"docstatus":1,
			"status": "Approved"

			})

		create_leave.insert()

		return create_leave
	
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

def weekoff_leave(year, month):
	current_year = datetime.now().year
	current_month = datetime.now().month
	weekoff_leave_data = frappe.db.sql("""
		SELECT employee, leave_type, from_date,total_leave_days
		FROM `tabLeave Application`
		WHERE leave_type = %s AND YEAR(from_date) = %s AND MONTH(from_date) = %s
	""", ("Week Off", current_year, current_month), as_dict=True)

	leave_info = {}

	# Count leaves and total_leave_days for each employee
	for emp in weekoff_leave_data:
		emp_id = emp['employee']
		leave_type = emp['leave_type']
		total_leave_days = emp['total_leave_days']

		if emp_id not in leave_info:
			leave_info[emp_id] = {'leave_count': 0, 'total_leave_days': 0}

		# If leave type is "Week Off", increment leave count
		if leave_type == "Week Off":
			leave_info[emp_id]['leave_count'] += 1
			leave_info[emp_id]['total_leave_days'] += total_leave_days

	# Check if any employee has exceeded the leave limit or total_leave_days
	for emp_id, info in leave_info.items():
		if info['total_leave_days'] > 2:
			frappe.throw(f"Employee {emp_id} has applied for more than two week off leaves in the specified month.")
		# if info['total_leave_days'] > 2:
		# 	frappe.throw(f"Employee {emp_id} has total leave days exceeding 2 in the specified month.")

	
	return leave_info


def notify_employee_on_submission(doc, method=None):
	if doc.workflow_state == "Pending" and not doc.custom_reason_for_rejection:
		frappe.msgprint("🎉 Attendance request has been successfully updated 🚀")
	if doc.workflow_state == "Approved":
		frappe.msgprint(f"Heyy 👩🏻‍💻!! The attendance request has been approved for {doc.employee_name}!! 📣")
	if doc.workflow_state == "Rejected" and not doc.custom_reason_for_rejection:
		frappe.throw("Please provide a reason for rejection before proceeding.")
	if doc.workflow_state == "Rejected":
		frappe.msgprint(f"🚨 Heyy 👩🏻‍💻!! The attendance request has been rejected for {doc.employee_name}!! 📣")

def notify_employee_comoff(doc,method=None):
	if doc.workflow_state == "Pending" and not doc.custom_reason_for_reject:
		frappe.msgprint(" 🎉 Your Compensatory Leave Request has been successfully updated 🚀")
	if doc.workflow_state == "Approved":
		frappe.msgprint(f"Heyy 👩🏻‍💻!! The Compensatory Leave Request has been approved for {doc.employee_name}!! 📣")
	if doc.workflow_state == "Rejected" and not doc.custom_reason_for_reject:
		frappe.throw("Please provide a reason for rejection before proceeding.")
	if doc.workflow_state == "Rejected":
		frappe.msgprint(f"🚨 Heyy 👩🏻‍💻!! The Compensatory Leave Request has been rejected for {doc.employee_name}!! 📣")



from datetime import datetime, timedelta

def Compensatory_off():
	today = datetime.now().date()
	
	thirty_days_ago = today - timedelta(days=30)
	delete_Compensatory_leave_request = frappe.db.get_list("Compensatory Leave Request", 
														   {"workflow_state": "Approved",
															"modified": ("<", thirty_days_ago)},
														   ['name'])

	for request in delete_Compensatory_leave_request:
		try:
			compensatory_doc = frappe.get_doc("Compensatory Leave Request", request.name)
			compensatory_doc.cancel()
			compensatory_doc.delete()
			frappe.db.commit()
		except Exception as e:
			frappe.log_error(f"Error deleting compensatory leave request {request.name}: {e}")


def capping_expense(doc, method=None):
	
	roles = frappe.get_roles()
	
	if "Report Manager" in roles and "Level Expense Approver" not in roles:
		if doc.workflow_state in ["Approve"]:
			expense_claim_details = frappe.get_all("Expense Claim Detail", filters={"parent": doc.name},fields=['custom_travel_type','amount'])
			for detail in expense_claim_details:
				if detail.get('custom_travel_type') == 'Flight' and detail.get('amount') > 5000:
						frappe.throw("You cannot approve this expense claim as the amount exceeds 5000. Please escalate for approval.")
				if detail.get('custom_travel_type') == 'Bus' and detail.get('amount') > 1500:
					frappe.throw("You cannot approve this expense claim as the amount exceeds 1500. Please escalate for approval.")		
				if detail.get('custom_travel_type') == 'Train' and detail.get('amount') > 1500:
					frappe.throw("You cannot approve this expense claim as the amount exceeds 2000. Please escalate for approval.")		
