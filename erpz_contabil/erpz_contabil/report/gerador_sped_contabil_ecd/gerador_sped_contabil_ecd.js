frappe.query_reports["Gerador SPED Contabil ECD"] = {
    "filters": [
        { "fieldname": "empresa", "label": __("Empresa"), "fieldtype": "Link", "options": "Company", "default": frappe.defaults.get_user_default("Company"), "reqd": 1 },
        { "fieldname": "from_date", "label": __("Data Inicial"), "fieldtype": "Date", "default": frappe.datetime.year_start(), "reqd": 1 },
        { "fieldname": "to_date", "label": __("Data Final"), "fieldtype": "Date", "default": frappe.datetime.get_today(), "reqd": 1 }
    ],

    "onload": function(report) {
        report.page.add_inner_button(__('Exportar Arquivo TXT (PVA SPED ECD)'), function() {
            let filters = report.get_values();
            frappe.dom.freeze(__('Gerando arquivo TXT do SPED Contábil ECD...'));
            frappe.call({
                method: 'erpz_contabil.erpz_contabil.report.gerador_sped_contabil_ecd.gerador_sped_contabil_ecd.baixar_arquivo_sped_ecd_txt',
                args: {
                    empresa: filters.empresa,
                    from_date: filters.from_date,
                    to_date: filters.to_date
                },
                callback: function(r) {
                    frappe.dom.unfreeze();
                    if (r.message && r.message.conteudo_txt) {
                        let blob = new Blob([r.message.conteudo_txt], { type: 'text/plain;charset=latin1' });
                        let link = document.createElement('a');
                        link.href = URL.createObjectURL(blob);
                        link.download = r.message.nome_arquivo || 'SPED_ECD.txt';
                        link.click();
                        frappe.show_alert({ message: __('Arquivo TXT do SPED ECD gerado com sucesso!'), indicator: 'green' });
                    }
                },
                error: function() {
                    frappe.dom.unfreeze();
                }
            });
        }).addClass('btn-primary');
    }
};

frappe.query_reports["Gerador SPED Contábil ECD"] = frappe.query_reports["Gerador SPED Contabil ECD"];
