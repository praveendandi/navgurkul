# import erpnext


import frappe
import erpnext
import frappe
from frappe import db
from datetime import date
from datetime import datetime
import frappe
from frappe.exceptions import ValidationError
from frappe.model.document import Document
from frappe import _
from hrms.hr.doctype.leave_application.leave_application import LeaveApplication


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
			frappe.msgprint(f"🚨 Heyy 👩🏻‍💻!! The Leave has been rejected for {self.employee_name}- {self.name}!! 📣")
				
			# self.satus = "Rejected"
		# except ValueError as e:
		# 	frappe.log_error(str(e))
		# 	return {"success": False, "data": str(e)}
		
		# return {"success": True, "data": "Validation successful"}
	
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
		timesheets = frappe.db.sql("""SELECT t.name,t.employee_name, t.month,t.workflow_state FROM `tabTime Tracker` as t""", as_dict=True) 

		# Calculate total hours for this employee
		for timesheet in timesheets:
			timesheet_hrs = frappe.db.sql("SELECT ts.date FROM `tabDaily TimeSheet` as ts WHERE `parent` = %s", timesheet.name, as_dict=True)
			
			# Convert each date string to datetime object and format month abbreviation
			for entry in timesheet_hrs:
				date_str = entry.get('date')
				if date_str:
					if isinstance(date_str, str):
						date = datetime.strptime(date_str, "%Y-%m-%d")
					else:
						date = datetime(date_str.year, date_str.month, date_str.day)
					teas_date = date.strftime("%b %Y")
					month = timesheet.month
					current_year = datetime.now().year
					month_year = f"{month} {current_year}"

					if month_year != teas_date:
						raise ValidationError("⚠️ Oops! Month and the date on the Timesheet has a mismatch. Please check. 😊")
					else: 
						pass  
		# Display success message once after the loop completes
		if doc.workflow_state == "Pending" and not doc.reason_for_reject:
			frappe.msgprint("🎉 Timesheet has been successfully updated 🚀")
				
		if doc.workflow_state == "Approve":
			frappe.msgprint(f"Heyy 👩🏻‍💻!! The time sheet has been approved for {doc.employee_name}- {doc.name}!! 📣")
			
		if doc.workflow_state == "Reject":
			reason_for_reject(doc)
			frappe.msgprint(f"🚨 Heyy 👩🏻‍💻!! The time sheet has been rejected for {doc.employee_name}- {doc.name}!! 📣")
				
					
		
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
	employee_ctc = frappe.db.get_list("Employee",{"name":name},['employee_name','ctc'])
	print(employee_ctc,"//99994444")
	return employee_ctc
