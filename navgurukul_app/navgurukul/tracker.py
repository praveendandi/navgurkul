# import frappe
# @frappe.whitelist()
# def send_mail_test():
#     users = frappe.get_all("User", fields=["name","email"])
#     get_temp = frappe.db.get_value("Email Template", "Time Sheet Approval Reminder", ["subject", "response"], as_dict=True)
#     employees = frappe.get_all("Employee", fields=["employee", "reporting_manager_name"])
#     for user in users:
#         roles = frappe.get_roles(user.name)
#         # print(roles,"\n\n",user.name)
#         if "Report Manager" in roles:
#             # print(user.name)
#             msg = frappe.render_template(get_temp["response"],{"reporting_manager_name":user.name})
#             # print("----------------------")
#             frappe.sendmail(
#                 recipients=user.email,
#                 subject=get_temp["subject"],
#                 message=msg,
#                 now=True
#             )
#             print(msg)
#             return msg

