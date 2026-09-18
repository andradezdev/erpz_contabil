import frappe

def setup_contabil_desktop_icon():
    icon_name = frappe.db.get_value("Desktop Icon", {"parent_icon": "Accounting", "link_to": "ERPZ Contábil"}, "name")
    if not icon_name:
        icon_name = frappe.db.get_value("Desktop Icon", {"label": "ERPZ Contábil"}, "name")
        
    if icon_name:
        frappe.db.set_value("Desktop Icon", icon_name, {
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
        })
    else:
        doc = frappe.new_doc("Desktop Icon")
        doc.name = "ERPZ Contabil Accounting"
        doc.label = "ERPZ Contábil"
        doc.icon = "calculator"
        doc.icon_type = "Link"
        doc.link_type = "Workspace Sidebar"
        doc.link_to = "ERPZ Contabil"
        doc.parent_icon = "Accounting"
        doc.hidden = 0
        doc.standard = 1
        doc.app = "erpz_contabil"
        doc.idx = 1
        doc.insert(ignore_permissions=True)

def after_install():
    setup_contabil_desktop_icon()
    frappe.db.commit()

def after_migrate():
    setup_contabil_desktop_icon()
    frappe.db.commit()
