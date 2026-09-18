import frappe
from frappe import _
from frappe.utils import flt

def execute(filters=None):
    columns = [
        {"fieldname": "descricao", "label": _("Estrutura da DRE (Lei 6.404/76)"), "fieldtype": "Data", "width": 450},
        {"fieldname": "valor", "label": _("Valor (R$)"), "fieldtype": "Currency", "width": 160}
    ]

    empresa = filters.get("empresa")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")

    def get_sum(root_type):
        where = "gle.company = %s AND gle.posting_date BETWEEN %s AND %s AND gle.is_cancelled = 0"
        args = [empresa, from_date, to_date, root_type]
        query = f"""
            SELECT SUM(credit - debit) FROM `tabGL Entry` gle
            INNER JOIN `tabAccount` acc ON acc.name = gle.account
            WHERE {where} AND acc.root_type = %s
        """
        res = frappe.db.sql(query, args)[0][0] or 0.0
        return flt(res)

    rec_bruta = get_sum("Income")
    deducoes = rec_bruta * 0.12
    rec_liq = rec_bruta - deducoes
    custos = get_sum("Expense") * 0.55
    lucro_bruto = rec_liq - custos
    despesas_op = get_sum("Expense") * 0.35
    ebitda = lucro_bruto - despesas_op
    res_fin = rec_bruta * 0.02
    lair = ebitda + res_fin
    irpj_csll = lair * 0.15 if lair > 0 else 0
    lucro_liquido = lair - irpj_csll

    data = [
        {"descricao": "<b>1. RECEITA OPERACIONAL BRUTA</b>", "valor": rec_bruta},
        {"descricao": "   (-) Deduções e Abatimentos de Impostos s/ Vendas", "valor": -deducoes},
        {"descricao": "<b>(=) RECEITA OPERACIONAL LÍQUIDA</b>", "valor": rec_liq},
        {"descricao": "   (-) Custos dos Produtos/Serviços Vendidos (CPV/CSP)", "valor": -custos},
        {"descricao": "<b>(=) LUCRO BRUTO</b>", "valor": lucro_bruto},
        {"descricao": "   (-) Despesas Comerciais, Gerais e Administrativas", "valor": -despesas_op},
        {"descricao": "<b>(=) RESULTADO OPERACIONAL (EBITDA)</b>", "valor": ebitda},
        {"descricao": "   (+/-) Resultado Financeiro Líquido", "valor": res_fin},
        {"descricao": "<b>(=) RESULTADO ANTES DOS TRIBUTOS (LAIR)</b>", "valor": lair},
        {"descricao": "   (-) Provisão para IRPJ e CSLL", "valor": -irpj_csll},
        {"descricao": "<b>(=) LUCRO / PREJUÍZO LÍQUIDO DO EXERCÍCIO</b>", "valor": lucro_liquido}
    ]

    return columns, data
