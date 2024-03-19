# import erpnext


import frappe
import erpnext
import frappe
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
    
from frappe import db

#

def total_hours_count(doc, method=None):
    # Get all unique employees
    print("///////////////")
    employees = db.sql("SELECT DISTINCT employee FROM `tabTime Tracker`", as_dict=True)

    for employee in employees:
        employee_name = employee.employee
        total_hours = 0

        # Get all timesheets for this employee
        timesheets = db.sql("SELECT * FROM `tabTime Tracker` WHERE employee = %s", employee_name, as_dict=True)

        # Calculate total hours for this employee
        for timesheet in timesheets:
            timesheet_hrs = db.sql("SELECT SUM(hours) FROM `tabDaily TimeSheet` WHERE `parent` = %s", timesheet.name)
            timesheet_hours = timesheet_hrs[0][0] if timesheet_hrs else 0
            total_hours += timesheet_hours

        # Update the total_hours field in the employee's document
        db.set_value("Time Tracker", {"employee": employee_name}, "total_hours", total_hours)
        doc.reload()
        print(total_hours, "total hours counted for,/////////////////", doc.name)

