# Copyright (c) 2024, nithinreddy and contributors
# For license information, please see license.txt

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
        # {"label": "Employer provident fund", "fieldtype": "Currency", "fieldname": "Employer provident fund", "width": 150},
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

    # print(final_result, "/9776555555")
    return final_result

# 
import re

def deductions_details(salary_earnings, salary_deductions, employee_ssa):

    final_deductions = {}
    for each in salary_deductions:
        
        pf_formula = each['formula'].split(' * ')
    
        for abr in salary_earnings:
            if abr["abbr"] == pf_formula[0]:
                pf_abbr = abr['formula'].split(" * ")
                pf_amount = abr['amount']
        formula_value = [float(s) for s in re.findall(r'\d.+', each['formula'])]
        # basic = employee_ssa[0]['base']/2
        if formula_value and employee_ssa[0]['base']/2:
            if employee_ssa[0]['base']/2 > 15000:
                print(employee_ssa[0]['base'],"///////4444444444")
                pf_rate = 1800
            else:
                pf_rate = employee_ssa[0]['base']/2 * 0.12
            
            component_name = f"{each['salary_component']}"
            final_deductions.update({component_name: (pf_rate )})

        elif formula_value and pf_amount:
            component_name = f"{each['salary_component']}"
            final_deductions.update({component_name: (float(pf_amount))})

        else:
            component_name = f"{each['salary_component']}"
            final_deductions.update({component_name: (each['amount'])})
            
    return final_deductions

