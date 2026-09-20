import frappe
import json, os

def setup_contabil_desktop_icon():
    icon_name = "ERPZ Contábil"
    acc_data = {
        "label": "ERPZ Contábil",
        "icon": "calculator",
        "icon_type": "Link",
        "link_type": "Workspace Sidebar",
        "link_to": "ERPZ Contábil",
        "parent_icon": "Accounting",
        "hidden": 0,
        "standard": 1,
        "app": "erpz_contabil",
        "idx": 1
    }

    if frappe.db.exists("Desktop Icon", icon_name):
        frappe.db.set_value("Desktop Icon", icon_name, acc_data)
    else:
        doc = frappe.new_doc("Desktop Icon")
        doc.update(acc_data)
        doc.insert(ignore_permissions=True)

    # Sincroniza Workspace Sidebar
    sb_file = "/home/frappe/frappe-bench/apps/erpz_contabil/erpz_contabil/workspace_sidebar/erpz_contabil.json"
    if os.path.exists(sb_file):
        with open(sb_file, "r", encoding="utf-8") as fp:
            sb_data = json.load(fp)

        if frappe.db.exists("Workspace Sidebar", "ERPZ Contábil"):
            sb = frappe.get_doc("Workspace Sidebar", "ERPZ Contábil")
            sb.items = []
            for it in sb_data.get("items", []):
                sb.append("items", it)
            sb.save(ignore_permissions=True)
        else:
            sb = frappe.new_doc("Workspace Sidebar")
            sb.update(sb_data)
            sb.insert(ignore_permissions=True)

def after_install():
    setup_contabil_desktop_icon()
    frappe.db.commit()

def after_migrate():
    setup_contabil_desktop_icon()
    frappe.db.commit()
