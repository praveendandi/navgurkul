# Copyright (c) 2024, nithinreddy and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data
# import frappe
# import re

# def execute(filters=None):
# 	try:
# 		conditions, data, final_earning, final_deduction = get_data(filters)
# 		columns = get_columns(final_earning, final_deduction)
# 		print(data,"dadadadadadaad")
# 		return columns,data, None
# 	except Exception as e:
# 		frappe.log_error(str(e))

# def get_columns(final_earning, final_deduction):
# 	columns = [
# 		{"label": "Employee", "fieldtype": "Link", "fieldname": "employee", "options": "Employee", "width": 150},
# 		{"label": "Employee Name", "fieldtype": "Data", "fieldname": "employee_name", "width": 150},
# 		{"label": "Company", "fieldtype": "Link", "fieldname": "company", "options": "Company", "width": 150},
# 		{"label": "Salary Structure", "fieldtype": "Link", "fieldname": "Salary Structure", "options": "Salary Structure", "width": 150},
# 		{"label": "Department", "fieldtype": "Data", "fieldname": "department", "width": 150},
# 		{"label": "Designation", "fieldtype": "Data", "fieldname": "designation", "width": 150},
# 	]

# 	unique_components = set()
# 	for employee_data in final_earning:
# 		unique_components.update(employee_data.keys() - {"Gross Amount"})

# 	unique_components = sorted(unique_components)

# 	for component in unique_components:
# 		columns.append(
# 			{
# 				"label": component.replace("_", " ").capitalize(),
# 				"fieldname": component,
# 				"fieldtype": "Currency",
# 				"width": 120,
# 			}
# 		)

# 	columns.append(
# 		{
# 			"label": "Gross Amount",
# 			"fieldname": "Gross Amount",
# 			"fieldtype": "Currency",
# 			"width": 120,
# 		}
# 	)

# 	ded_unique_components = set()
# 	for employee_data in final_deduction:
# 		ded_unique_components.update(employee_data.keys())

# 	ded_unique_components = sorted(ded_unique_components)
# 	for component_ded in ded_unique_components:
# 		columns.append(
# 			{
# 				"label": component_ded.replace("_", " ").capitalize(),
# 				"fieldname": component_ded,
# 				"fieldtype": "Currency",
# 				"width": 120,
# 			}
# 		)
# 	columns.append(
# 		{
# 			"label": "Net Amount",
# 			"fieldname": "net_pay",
# 			"fieldtype": "Currency",
# 			"width": 120,
# 		}
# 	)

# 	return columns

# def get_data(filters):
# 	try:
# 		print("///////////////")
# 		conditions = get_conditions(filters)

# 		columns_deduction = []
# 		columns_earning = []
# 		final_data = []
# 		duplicate_earning = None

# 		if filters.get("employee"):
# 			filters_emp = {"status": "Active", 'employee': filters.get("employee")}
# 		else:
# 			filters_emp = {"status": "Active"}

# 		if filters.get("department"):
# 			filters_emp.update({'department': filters.get("department")})
            
# 		if filters.get("company"):
# 			filters_emp.update({'company': filters.get("company")})

# 		employee_list = frappe.db.get_list("Employee", filters_emp, ['employee', 'company', 'department', 'designation', 'employee_name'], order_by='employee asc')
# 		# print(employee_list,"/////009999999999")
# 		for each in employee_list:
# 			if not filters.get("salary_structure"):
# 				filters_data = {'employee': each['employee'], 'docstatus': 1}
# 			else:
# 				filters_data = {'employee': each['employee'], 'docstatus': 1, "salary_structure": filters.get("salary_structure")}

# 			employee_ssa = frappe.db.get_list("Salary Structure Assignment", filters_data, ['employee', 'salary_structure', 'base'])
# 			# print(employee_ssa,"655545678765434567")
# 			if len(employee_ssa) > 0:
# 				salary_earnings = frappe.get_doc("Salary Detail", {'parent': employee_ssa[0]['salary_structure'], 'parentfield': "earnings"}).as_dict()
# 				salary_deductions = frappe.get_doc("Salary Detail", {'parent': employee_ssa[0]['salary_structure'], 'parentfield': "deductions"}).as_dict()
# 				print(salary_earnings,"pppppppppppppppppppp")
# 				earning = earnings_details(salary_earnings, employee_ssa)
# 				# print(earning,"555555555555")
# 				# duplicate_earning = earning.copy()

# 				columns_earning.append(duplicate_earning)
                
# 				deductions = deductions_details(salary_earnings,salary_deductions,employee_ssa)
# 				total_deduction = 0
# 				for component in deductions.values():
# 					total_deduction += component
# 				deductions.update({"total_deduction": total_deduction})

# 				columns_deduction.append(deductions)
# 				for i in employee_ssa:
# 					value = i.get("salary_structure")
# 					earning.update({'Salary Structure': value})
# 				earning.update({"employee": each['employee'], "employee_name": each['employee_name'], "department": each['department'],
# 								"designation": each['designation'],"company": each['company']})
# 				earning.update(deductions)

# 				final_data.append(earning)
# 				for i in final_data:
# 					net_pay = i.get("Gross Amount") - i.get("total_deduction")
# 					i.update({"net_pay": net_pay})
# 		# print(final_data,"/////////////////")
# 		return conditions, final_data, columns_earning, columns_deduction

# 	except Exception as e:
# 		frappe.log_error(str(e))

# def earnings_details(salary_earnings, employee_ssa):
# 	try:
# 		print(salary_earnings,"earnings_detailsearnings_detailsearnings_detailsearnings_details")
# 		final_result = {"Gross Amount": 0.0}

# 		for each in salary_earnings:
# 			print(each[0]['formula'],"88888888888")
# 			value_formula = 0.0 
# 			if "/" in each['formula']:
# 				print("ififififififfiifififfifi")
# 				abbr_formula_values = each['formula'].split(' / ') 

# 			for abr in salary_earnings:
                
# 				if abr["abbr"] == abbr_formula_values[0]:
# 					formula_value = abr['formula'].split("*")[1]
# 					value_formula = float(formula_value) / int(abbr_formula_values[1])
                    
# 				each['formula'] = f"base * {value_formula}"
            
# 			formula_value = [float(s) for s in re.findall(r'\d.+', each['formula'])]
# 			print(formula_value,"/////////777/////////")
# 			if formula_value:
# 				component_name = each['salary_component']
# 				final_result.update({component_name: (employee_ssa[0]['base'] * formula_value[0])})
# 				final_result["Gross Amount"] += employee_ssa[0]['base'] * formula_value[0]
# 			else:
# 				component_name = each['salary_component']
# 				final_result.update({component_name: each['amount']})
# 				final_result["Gross Amount"] += each['amount']
# 		print(final_result,"/9776555555")
# 		return final_result
    
# 	except Exception as e:
# 		frappe.log_error(str(e))

# def deductions_details(salary_earnings,salary_deductions,employee_ssa):
# 	try:
# 		final_deductions = {}
# 		for each in salary_deductions:
            
# 			pf_formula = each['formula'].split(' * ')
        
# 			for abr in salary_earnings:
# 				if abr["abbr"] == pf_formula[0]:
# 					pf_abbr = abr['formula'].split(" * ")
# 					pf_amount = abr['amount']
# 			formula_value = [float(s) for s in re.findall(r'\d.+', each['formula'])]

# 			if formula_value and employee_ssa[0]['base']:
# 				component_name = f"{each['salary_component']}"
# 				final_deductions.update({component_name: (employee_ssa[0]['base'] * float(pf_abbr[1])* formula_value[0])})

# 			elif formula_value and pf_amount:
# 				component_name = f"{each['salary_component']}"
# 				final_deductions.update({component_name: (float(pf_amount) * formula_value[0])})

# 			else:
# 				component_name = f"{each['salary_component']}"
# 				final_deductions.update({component_name: (each['amount'])})
                
# 		return final_deductions
    
# 	except Exception as e:
# 		frappe.log_error(str(e))

# def get_conditions(filters):
# 	try:
# 		conditions = ""
        
# 		if filters.get("company"):
# 			conditions += " and company = '%s'" % filters.get("company")
# 		if filters.get("salary_structure"):
# 			conditions += " and salary_structure = '%s'" % filters.get("salary_structure")
# 		if filters.get("employee"):
# 			conditions += " and employee = '%s'" % filters.get("employee")
# 		if filters.get("department"):
# 			conditions += " and department = '%s'" % filters.get("department")
            
# 		return conditions
    
# 	except Exception as e:
# 		frappe.log_error(str(e))
import frappe 
import re

def execute(filters=None):
# 	try:
        data = get_data(filters)
        columns = get_columns()
        return columns,data, None
# 	except Exception as e:
# 		frappe.log_error(str(e))

def get_columns():
    columns = [
        {"label": "Employee", "fieldtype": "Link", "fieldname": "employee", "options": "Employee", "width": 150},
        {"label": "Employee Name", "fieldtype": "Data", "fieldname": "employee_name", "width": 150},
        {"label": "Company", "fieldtype": "Link", "fieldname": "company", "options": "Company", "width": 150},
        # {"label": "Salary Structure", "fieldtype": "Link", "fieldname": "Salary Structure", "options": "Salary Structure", "width": 150},
        {"label": "Department", "fieldtype": "Data", "fieldname": "department", "width": 150},
        {"label": "Designation", "fieldtype": "Data", "fieldname": "designation", "width": 150},
        {"label": "Work Location Type", "fieldtype": "Data", "fieldname": "custom_work_location_type", "width": 150},
        {"label": "Basic", "fieldtype": "Currency", "fieldname": "basic", "width": 150},
        {"label": "House Rent Allowance", "fieldtype": "Currency", "fieldname": "House Rent Allowance", "width": 150},
        {"label": "Coordinator Allowance", "fieldtype": "Currency", "fieldname": "Coordinator Allowance", "width": 150},
        {"label": "Other Allowance", "fieldtype": "Currency", "fieldname": "other_allowance", "width": 150},
        {"label": "Gross Amount", "fieldtype": "Currency", "fieldname": "Gross Amount", "width": 150},
        {"label": "Provident Fund", "fieldtype": "Currency", "fieldname": "Provident Fund", "width": 150},
        {"label": "Employer provident fund", "fieldtype": "Currency", "fieldname": "Employer provident fund", "width": 150},
        {"label": "Total Deduction", "fieldtype": "Currency", "fieldname": "total_deduction", "width": 150},
        {"label": "Netpay", "fieldtype": "Currency", "fieldname": "net_pay", "width": 150}

    ]
    return columns

def get_data(filters):
    
    final_data = []

    employee_list = frappe.db.get_list("Employee", {"status": "Active"}, ['employee', 'company', 'department', 'designation', 'employee_name','custom_work_location_type'], order_by='employee asc')
    for each in employee_list:

        employee_ssa = frappe.db.get_list("Salary Structure Assignment", {'employee': each['employee'], 'docstatus': 1}, ['employee', 'salary_structure', 'base'])
        # print(employee_ssa,"655545678765434567")
        if len(employee_ssa) > 0:
            # print(employee_ssa,"655545678765434567")
            salary_earnings = frappe.get_all("Salary Detail", filters={'parent': employee_ssa[0]['salary_structure'], 'parentfield': "earnings"},fields=["*"],order_by="idx ASC")
            
            salary_deductions = frappe.get_all("Salary Detail", filters = {'parent': employee_ssa[0]['salary_structure'], 'parentfield': "deductions"},fields=["*"],order_by="idx ASC")
            earning = earnings_details(salary_earnings, employee_ssa)
            deductions = deductions_details(salary_earnings,salary_deductions,employee_ssa)
            total_deduction = 0
            for component in deductions.values():
                total_deduction += component
            deductions.update({"total_deduction": total_deduction})
            earning.update({"employee": each['employee'], "employee_name": each['employee_name'], "department": each['department'],
								"designation": each['designation'],"company": each['company'],"custom_work_location_type":each['custom_work_location_type']})
            earning.update(deductions)
            final_data.append(earning)
            for i in final_data:
                net_pay = i.get("Gross Amount") - i.get("total_deduction")
                i.update({"net_pay": net_pay})
    # print(final_data,"999999999999999999")
    return final_data

def earnings_details(salary_earnings, employee_ssa):

    if not all(isinstance(entry, dict) for entry in salary_earnings):
        raise ValueError("salary_earnings must be a list of dictionaries")
    if not all(isinstance(entry, dict) for entry in employee_ssa):
        raise ValueError("employee_ssa must be a list of dictionaries")

    final_result = {}
    basic_B = 0.0

    for each in salary_earnings:
    
        if "base" in each['formula'] and each['abbr'] == "B":
    
            abbr_formula_values = each['formula'].split("*")
            basic_B ,basic= round(employee_ssa[0]['base'] * float(abbr_formula_values[1]),2),round(employee_ssa[0]['base'] * float(abbr_formula_values[1]),2)

            final_result.update({"basic":basic})           

            final_result.setdefault("Gross Amount", 0)
            final_result["Gross Amount"] += round(employee_ssa[0]['base'] * float(abbr_formula_values[1]),2)

        if "base" in each['formula'] and each['abbr'] == "OA":

            component_name = each['salary_component'].lower().replace(" ","_")
            abbr_formula_values = each['formula'].split("*")
            
            final_result.update({component_name: round(employee_ssa[0]['base'] * float(abbr_formula_values[1]),2)})

            final_result.setdefault("Gross Amount", 0.0)
            final_result["Gross Amount"] += round(employee_ssa[0]['base'] * float(abbr_formula_values[1]),2)
        
        if "B" in each['formula'] and "base" not in each['formula']:
            formula_value = [float(s) for s in re.findall(r'\d.+', each['formula'])]
            if formula_value:
                component_name = each['salary_component']
                final_result.update({component_name: ( basic_B* formula_value[0])})
                final_result.setdefault("Gross Amount", 0)
                final_result["Gross Amount"] += basic_B * formula_value[0]
        else:
            component_name = each['salary_component']
            final_result.update({component_name: each['amount']})
            final_result.setdefault("Gross Amount", 0)
            final_result["Gross Amount"] += each['amount']

    print(final_result, "/9776555555")
    return final_result

def deductions_details(salary_earnings,salary_deductions,employee_ssa):

    final_deductions = {}
    for each in salary_deductions:
        
        pf_formula = each['formula'].split(' * ')
    
        for abr in salary_earnings:
            if abr["abbr"] == pf_formula[0]:
                pf_abbr = abr['formula'].split(" * ")
                pf_amount = abr['amount']
        formula_value = [float(s) for s in re.findall(r'\d.+', each['formula'])]

        if formula_value and employee_ssa[0]['base']:
            component_name = f"{each['salary_component']}"
            final_deductions.update({component_name: (employee_ssa[0]['base'] * float(pf_abbr[1])* formula_value[0])})

        elif formula_value and pf_amount:
            component_name = f"{each['salary_component']}"
            final_deductions.update({component_name: (float(pf_amount) * formula_value[0])})

        else:
            component_name = f"{each['salary_component']}"
            final_deductions.update({component_name: (each['amount'])})
            
    return final_deductions




# import re

# def earnings_details(salary_earnings, employee_ssa):
#     if not all(isinstance(entry, dict) for entry in salary_earnings):
#         raise ValueError("salary_earnings must be a list of dictionaries")
#     if not all(isinstance(entry, dict) for entry in employee_ssa):
#         raise ValueError("employee_ssa must be a list of dictionaries")

#     final_result = {}
#     basic_B = 0.0

#     for each in salary_earnings:
#         if "B" not in each['formula'] and each['abbr'] == "B":
#             abbr_formula_values = each['formula'].split("*")
#             basic_B = round(employee_ssa[0]['base'] * float(abbr_formula_values[1]), 2)
#             component_name = each['salary_component']
#             final_result[component_name] = basic_B
#             final_result.setdefault("Gross Amount", 0)
#             final_result["Gross Amount"] += basic_B

#         elif "B" not in each['formula'] and each['abbr'] != "B":
#             abbr_formula_values = each['formula'].split("*")
#             amount = round(employee_ssa[0]['base'] * float(abbr_formula_values[1]), 2)
#             component_name = each['salary_component']
#             final_result[component_name] = amount
#             final_result.setdefault("Gross Amount", 0)
#             final_result["Gross Amount"] += amount

#         elif "B" in each['formula']:
#             formula_value = float(re.findall(r'\d+', each['formula'])[0])
#             amount = round(basic_B * formula_value, 2)
#             component_name = each['salary_component']
#             final_result[component_name] = amount
#             final_result.setdefault("Gross Amount", 0)
#             final_result["Gross Amount"] += amount

#     # Ensure all components are included, even if their values are zero
#     for component in salary_earnings:
#         if component['salary_component'] not in final_result:
#             final_result[component['salary_component']] = 0.0

#     # Add missing components with zero values
#     if component in salary_earnings:
#         for component in salary_earnings:
#             if component['salary_component'] not in final_result:
#                 final_result[component['salary_component']] = 0.0
#     else:
#          for component in salary_earnings:
#             if component['salary_component'] not in final_result:
#                 final_result[component['salary_component']] = 0.0

#     return final_result

# import re

# def earnings_details(salary_earnings, employee_ssa):
#     if not all(isinstance(entry, dict) for entry in salary_earnings):
#         raise ValueError("salary_earnings must be a list of dictionaries")
#     if not all(isinstance(entry, dict) for entry in employee_ssa):
#         raise ValueError("employee_ssa must be a list of dictionaries")

#     final_result = {}
#     basic_B = 0.0

#     for each in salary_earnings:
#         abbr_formula_values = each['formula'].split("*")
#         component_name = each['salary_component']

#         if "B" not in each['formula'] and each['abbr'] == "B":
#             abbr_formula_values = each['formula'].split("*")
#             basic_B = round(employee_ssa[0]['base'] * float(abbr_formula_values[1]), 2)

#         if "B" not in each['formula']:
#             final_result.setdefault(component_name, 0.0)
#             if each['abbr'] == "B":
#                 final_result[component_name] = basic_B
#             else:
#                 final_result[component_name] = round(employee_ssa[0]['base'] * float(abbr_formula_values[1]), 2)
#             final_result.setdefault("Gross Amount", 0)
#             final_result["Gross Amount"] += final_result[component_name]

#         elif "B" in each['formula']:
#             formula_value = [float(s) for s in re.findall(r'\d+', each['formula'])]
#             final_result.setdefault(component_name, 0.0)
#             final_result[component_name] = (basic_B * formula_value[0])
#             final_result.setdefault("Gross Amount", 0)
#             final_result["Gross Amount"] += final_result[component_name]

#     # Ensure all components are present in the final result even if their values are zero
#     all_components = set(each['salary_component'] for each in salary_earnings)
#     for component in all_components:
#         if component not in final_result:
#             final_result[component] = 0.0

#     return final_result


# import re

# def earnings_details(salary_earnings, employee_ssa):
#     if not all(isinstance(entry, dict) for entry in salary_earnings):
#         raise ValueError("salary_earnings must be a list of dictionaries")
#     if not all(isinstance(entry, dict) for entry in employee_ssa):
#         raise ValueError("employee_ssa must be a list of dictionaries")

#     final_result = {}

#     for each in salary_earnings:
        
#         formula_value = [float(s) for s in re.findall(r'\d.+', each['formula'])]

#         # Check if formula_value is non-empty
#         if formula_value:
#             component_name = each['salary_component']
#             final_result.update({component_name: (employee_ssa[0]['base'] * formula_value[0])})
#             final_result.setdefault("Gross Amount", 0)
#             final_result["Gross Amount"] += employee_ssa[0]['base'] * formula_value[0]
#         else:
#             component_name = each['salary_component']
#             final_result.update({component_name: each['amount']})
#             final_result.setdefault("Gross Amount", 0)
#             final_result["Gross Amount"] += each['amount']

#     return final_result
