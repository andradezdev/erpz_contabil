import frappe
import json, os

def setup_contabil_desktop_icon():
    icon_name = "ERPZ Contabil"
    acc_data = {
        "label": "ERPZ Contabil",
        "icon": "calculator",
        "icon_type": "Link",
        "link_type": "Workspace Sidebar",
        "link_to": "ERPZ Contabil",
        "parent_icon": "",
        "hidden": 0,
        "standard": 1,
        "app": "erpz_contabil",
        "idx": 10
    }

    if frappe.db.exists("Desktop Icon", icon_name):
        frappe.db.set_value("Desktop Icon", icon_name, acc_data)
    else:
        doc = frappe.new_doc("Desktop Icon")
        doc.name = icon_name
        doc.update(acc_data)
        doc.insert(ignore_permissions=True)

    # Sincroniza Workspace Sidebar
    sb_file = "/home/frappe/frappe-bench/apps/erpz_contabil/erpz_contabil/workspace_sidebar/erpz_contabil.json"
    if os.path.exists(sb_file):
        with open(sb_file, "r", encoding="utf-8") as fp:
            sb_data = json.load(fp)

        if frappe.db.exists("Workspace Sidebar", "ERPZ Contabil"):
            sb = frappe.get_doc("Workspace Sidebar", "ERPZ Contabil")
            sb.items = []
            for it in sb_data.get("items", []):
                sb.append("items", it)
            sb.save(ignore_permissions=True)
        else:
            sb = frappe.new_doc("Workspace Sidebar")
            sb.update(sb_data)
            sb.insert(ignore_permissions=True)

    # Atualiza Desktop Layout se o usuario ja possuir layout salvo
    if frappe.db.table_exists("Desktop Layout"):
        layouts = frappe.get_all("Desktop Layout", fields=["name", "layout"])
        for l in layouts:
            if not l.layout:
                continue
            try:
                items = json.loads(l.layout)
                has_it = any(x.get("name") == icon_name or x.get("label") == icon_name for x in items)
                if not has_it:
                    c_item = {
                        "label": "ERPZ Contabil",
                        "bg_color": "gray",
                        "link": None,
                        "link_type": "Workspace Sidebar",
                        "app": "erpz_contabil",
                        "icon_type": "Link",
                        "parent_icon": "",
                        "icon": "calculator",
                        "link_to": "ERPZ Contabil",
                        "idx": 10,
                        "standard": 1,
                        "logo_url": None,
                        "hidden": 0,
                        "name": "ERPZ Contabil",
                        "restrict_removal": 0,
                        "icon_image": None
                    }
                    items.append(c_item)
                    doc_l = frappe.get_doc("Desktop Layout", l.name)
                    doc_l.layout = json.dumps(items)
                    doc_l.save(ignore_permissions=True)
            except Exception:
                pass

def after_install():
    setup_contabil_desktop_icon()
    frappe.db.commit()

def after_migrate():
    setup_contabil_desktop_icon()
    frappe.db.commit()
