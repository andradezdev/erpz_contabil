import frappe
from frappe import _

def execute(filters=None):
    columns = [
        {"fieldname": "linha_sped", "label": _("Registro SPED ECD (Linha Oficial)"), "fieldtype": "Data", "width": 800}
    ]
    empresa = filters.get("empresa")
    from_date = (filters.get("from_date") or "").replace("-", "")
    to_date = (filters.get("to_date") or "").replace("-", "")

    linhas = [
        f"|0000|LECD|{from_date}|{to_date}|{empresa[:60]}|12345678000195|SP|123456789|3550308||0|0|N|||",
        "|0001|0|",
        "|0007|00|00|",
        "|0990|4|",
        "|I001|0|",
        "|I010|G|1.00|",
        "|I030|TERMO DE ABERTURA|1|LIVRO DIARIO GERAL|100||||||||",
        "|I990|4|",
        "|J001|0|",
        "|J005|01012026|31122026|1|BALANCO PATRIMONIAL E DRE|",
        "|J990|3|",
        "|9001|0|",
        f"|9999|13|"
    ]

    return columns, [{"linha_sped": l} for l in linhas]
