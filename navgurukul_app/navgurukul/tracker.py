# import frappe
# @frappe.whitelist()
# def send_mail_test():
#     users = frappe.get_all("User")
#     # print(users)
#     for user in users:
#         roles = frappe.get_roles(user.name)
#         # print(roles, "||||||||||||||||||||||")
#         if "Report Manager" in roles:
#             get_temp=frappe.db.get_value("Email Template","Time Sheet Approval Reminder",["subject","response"], as_dict=True)
#             # print(get_temp,"---------------")
#             if get_temp:  # Check if the template was found
#                 employees = frappe.get_all("Employee", fields=["employee"])
#                 # print(employees,"|||||||||||")
#                 for employee in employees:
#                     # print(employee.employee, "+++++++++++++++++++++++++++++")
#                     get_record = frappe.db.get_value("Employee", employee.employee, fields=["reporting_manager_name"], as_dict=True)
#                     print(get_record,"-------------------")
#     #                 if get_record:  # Check if the record was found
#     #                     msg = frappe.render_template(get_temp["response"], get_record)
#                         # print(msg)
#                         # if user.name == get_record["reporting_manager_name"]:
#                         #     frappe.sendmail(
#                         #         recipients=user.name,
#                         #         subject=get_temp["subject"],
#                         #         message=msg,
#                         #         now=True
#                         #     )
#                         #     print("--------------------------")


