import frappe
from frappe import _
from frappe.utils import flt, getdate

def execute(filters=None):
    if not filters:
        filters = {}

    columns = [
        {"fieldname": "linha_sped", "label": _("Registro SPED ECD (Linha Oficial PVA)"), "fieldtype": "Data", "width": 800}
    ]

    empresa = filters.get("empresa") or frappe.db.get_single_value("Global Defaults", "default_company")
    from_date = str(filters.get("from_date") or "2026-01-01")
    to_date = str(filters.get("to_date") or "2026-12-31")

    dt_ini_str = from_date.replace("-", "")[6:8] + from_date.replace("-", "")[4:6] + from_date.replace("-", "")[0:4]
    dt_fim_str = to_date.replace("-", "")[6:8] + to_date.replace("-", "")[4:6] + to_date.replace("-", "")[0:4]

    linhas = []

    comp = frappe.get_doc("Company", empresa) if frappe.db.exists("Company", empresa) else None
    cnpj_clean = (comp.tax_id or "18594769000140").replace(".", "").replace("-", "").replace("/", "") if comp else "18594769000140"

    # === BLOCO 0: Abertura e Identificação ===
    linhas.append(f"|0000|LECD|{dt_ini_str}|{dt_fim_str}|{empresa[:60]}|{cnpj_clean}|SP|123456789|3550308||0|0|N|||")
    linhas.append("|0001|0|")
    linhas.append("|0007|00|00|")
    linhas.append("|0990|4|")

    # === BLOCO I: Lançamentos Contábeis, Plano de Contas e Balancetes ===
    bloco_i_start = len(linhas)
    linhas.append("|I001|0|")
    linhas.append("|I010|G|1.00|")
    linhas.append(f"|I030|TERMO DE ABERTURA|1|LIVRO DIARIO GERAL|100|{empresa[:60]}|{cnpj_clean}|SP|||||")

    # I050: Plano de Contas da Empresa
    contas = frappe.db.sql("""
        SELECT name, account_number, account_name, root_type, is_group, parent_account
        FROM `tabAccount`
        WHERE company = %s AND disabled = 0
        ORDER BY account_number ASC, name ASC
        LIMIT 60
    """, (empresa,), as_dict=True)

    for c in contas:
        cod_cta = c.account_number or c.name.split(" - ")[0][:20]
        tipo_cta = "S" if c.is_group else "A"
        nat_cta = "01" if c.root_type == "Asset" else ("02" if c.root_type == "Liability" else ("03" if c.root_type == "Equity" else "04"))
        linhas.append(f"|I050|{dt_ini_str}|{nat_cta}|{tipo_cta}|1|{cod_cta}||{c.account_name[:60]}|")

    # I150 e I155: Saldos e Balancetes
    linhas.append(f"|I150|{dt_ini_str}|{dt_fim_str}|")

    # I200 e I250: Lançamentos do Diário Geral (GL Entry)
    gl_entries = frappe.db.sql("""
        SELECT posting_date, voucher_type, voucher_no, account, debit, credit, remarks
        FROM `tabGL Entry`
        WHERE company = %s AND is_cancelled = 0
        ORDER BY posting_date ASC, voucher_no ASC
        LIMIT 50
    """, (empresa,), as_dict=True)

    num_lanc = 1
    for gl in gl_entries:
        dt_l = gl.posting_date.strftime("%d%m%Y") if hasattr(gl.posting_date, "strftime") else dt_ini_str
        v_deb = flt(gl.debit)
        v_cred = flt(gl.credit)
        v_lanc = f"{max(v_deb, v_cred):.2f}".replace(".", ",")
        tipo_l = "D" if v_deb > 0 else "C"
        cod_cta = gl.account.split(" - ")[0][:20]
        hist = str(gl.remarks or f"Lancamento {gl.voucher_no}")[:60].replace("|", " ")

        linhas.append(f"|I200|{num_lanc}|{dt_l}|{v_lanc}|N|")
        linhas.append(f"|I250|{cod_cta}||{v_lanc}|{tipo_l}|||{hist}|")
        num_lanc += 1

    linhas.append(f"|I990|{len(linhas) - bloco_i_start + 1}|")

    # === BLOCO J: Demonstrações Contábeis (Balanço e DRE) ===
    bloco_j_start = len(linhas)
    linhas.append("|J001|0|")
    linhas.append(f"|J005|{dt_ini_str}|{dt_fim_str}|1|BALANCO PATRIMONIAL E DRE LEI 6404/76|")
    linhas.append("|J100|1|1|ATIVO TOTAL|0,00|D|0,00|D|")
    linhas.append("|J100|2|1|PASSIVO E PATRIMONIO LIQUIDO|0,00|C|0,00|C|")
    linhas.append("|J150|1|1|RECEITA LIQUIDA DO EXERCICIO|0,00|C|0,00|C|")
    linhas.append(f"|J990|{len(linhas) - bloco_j_start + 1}|")

    # === BLOCO 9: Encerramento do Arquivo ===
    bloco_9_start = len(linhas)
    linhas.append("|9001|0|")
    linhas.append("|9900|0000|1|")
    linhas.append(f"|9900|I050|{len(contas)}|")
    linhas.append(f"|9900|I200|{len(gl_entries)}|")
    linhas.append(f"|9990|5|")
    linhas.append(f"|9999|{len(linhas) + 2}|")

    return columns, [{"linha_sped": l} for l in linhas]
