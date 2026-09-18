frappe.query_reports["Gerador SPED Contabil ECD"] = {
    "filters": [
        { "fieldname": "empresa", "label": __("Empresa"), "fieldtype": "Link", "options": "Company", "default": frappe.defaults.get_user_default("Company"), "reqd": 1 },
        { "fieldname": "from_date", "label": __("Data Inicial"), "fieldtype": "Date", "default": frappe.datetime.year_start(), "reqd": 1 },
        { "fieldname": "to_date", "label": __("Data Final"), "fieldtype": "Date", "default": frappe.datetime.get_today(), "reqd": 1 }
    ]
};
