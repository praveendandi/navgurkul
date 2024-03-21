# import erpnext


import frappe
import erpnext
import frappe
from frappe import db
from datetime import datetime
from datetime import date
from frappe.model.document import Document
from frappe import _
from hrms.hr.doctype.leave_application.leave_application import LeaveApplication


class LeaveApplication2(LeaveApplication):
	def validate(self):
		super().validate()
		self.before_submit()
	
	def before_submit(self):
		if self.workflow_state == 'Reject':
			validation_result = self.validate_before_rejection('reject')
			if not validation_result["success"]:
				frappe.throw(validation_result["data"])
			else:
				pass
				# self.workflow_state = "Rejected"
				# self.status = "Rejected"
				# self.save()
				# self.reload()

	def validate_before_rejection(self, action):
		try:
			if action == 'reject' and not self.custom_reason_for_cancel:
				raise ValueError("Please provide a reason for rejection before proceeding.")
			# self.satus = "Rejected"
		except ValueError as e:
			frappe.log_error(str(e))
			return {"success": False, "data": str(e)}
		
		return {"success": True, "data": "Validation successful"}
	
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
		timesheets = db.sql("""SELECT t.name, t.month FROM `tabTime Tracker` as t""", as_dict=True)
		
		# Calculate total hours for this employee
		for timesheet in timesheets:
			timesheet_hrs = db.sql("SELECT ts.date FROM `tabDaily TimeSheet` as ts WHERE `parent` = %s", timesheet.name, as_dict=True)
			
			# Convert each date string to datetime object and format month abbreviation
			for entry in timesheet_hrs:
				date_str = entry.get('date')
				if date_str:
					if isinstance(date_str, str):
						date = datetime.strptime(date_str, "%Y-%m-%d")
					else:
						date = datetime(date_str.year, date_str.month, date_str.day)
					formatted_date = date.strftime("%b")
				
					month = timesheet.month
					
					if month != formatted_date:
						frappe.throw("The month in your timesheet doesn't match the formatted date")
					
					
				else:
					print("No date found for timesheet:", timesheet.name)
		if month == formatted_date:
			frappe.msgprint("🎉 Your timesheet has been successfully updated! 🚀")
	except Exception as e:
		print("An error occurred:", e)		


from datetime import datetime

def employee_age_current_experience(doc, method=None):
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
				frappe.db.set_value('Employee', name, 'custom_current_experience', current_experience)

			# Calculate age based on date_of_birth
			if date_of_birth:
				age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
				frappe.db.set_value('Employee', name, 'custom_age', age)
	except Exception as e:
		print("An error occurred:", e)	