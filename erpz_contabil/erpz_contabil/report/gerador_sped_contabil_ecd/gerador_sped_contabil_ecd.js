frappe.query_reports["Gerador SPED Contabil ECD"] = {
    "filters": [
        { "fieldname": "empresa", "label": __("Empresa"), "fieldtype": "Link", "options": "Company", "default": frappe.defaults.get_user_default("Company"), "reqd": 1 },
        { "fieldname": "from_date", "label": __("Data Inicial"), "fieldtype": "Date", "default": frappe.datetime.year_start(), "reqd": 1 },
        { "fieldname": "to_date", "label": __("Data Final"), "fieldtype": "Date", "default": frappe.datetime.get_today(), "reqd": 1 }
    ],

    "onload": function(report) {
        // Botão para baixar diretamente o arquivo TXT pronto para importar no PVA da Receita Federal
        report.page.add_inner_button(__('Exportar Arquivo TXT (PVA SPED ECD)'), function() {
            let data = report.data;
            if (!data || data.length === 0) {
                frappe.msgprint(__('Nenhum dado gerado para exportar.'));
                return;
            }
            let txt = data.map(d => d.linha_sped).join('\r\n') + '\r\n';
            let blob = new Blob([txt], { type: 'text/plain;charset=latin1' });
            let link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            let filters = report.get_values();
            link.download = 'SPED_ECD_' + (filters.empresa || 'EMPRESA') + '_' + frappe.datetime.get_today().replace(/-/g, '') + '.txt';
            link.click();
            frappe.show_alert({ message: __('Arquivo TXT do SPED ECD gerado com sucesso!'), indicator: 'green' });
        }).addClass('btn-primary');
    }
};
