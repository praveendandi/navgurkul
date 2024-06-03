import frappe
@frappe.whitelist()
def send_mail_test():
	try:
		users = frappe.get_all("User", fields=["name", "email", "username"])
		email_template = frappe.db.get_value("Email Template", "Time Sheet Approval Reminder", ["subject", "response"], as_dict=True)
		if not email_template:
			print("Email Template not found")
		for user in users:
			roles = frappe.get_roles(user.name)
			if "Report Manager" in roles:
				# print(roles)
				msg = frappe.render_template(email_template["response"], {"report_manager": user["username"]})
				frappe.sendmail(
					recipients=user["email"], 
					subject=email_template["subject"],
					message=msg,
					now=True
				)

				# print(msg)
				return "Emails sent successfully"
	except Exception as e:
		print("ERROR :",e)


