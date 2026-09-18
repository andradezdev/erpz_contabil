# ERPZ Contábil — Contabilidade Societária, DRE Lei 6.404/76 e SPED Contábil ECD

Solução corporativa de **Contabilidade Societária e Fiscal Brasileira** desenvolvida nativamente para o **Frappe Framework** e **ERPNext** (v16), perfeitamente integrada ao módulo de Contabilidade (`Accounting`), contemplando a DRE oficial estruturada pela Lei das Sociedades por Ações (Lei 6.404/76), Plano de Contas Referencial da Receita Federal do Brasil (RFB) e geração do SPED Contábil ECD.

---

## Sumário Executivo

O **ERPZ Contábil** traduz as movimentações financeiras e lançamentos de diário (`Journal Entry` e `GL Entry`) do ERPNext para o rigor das normas contábeis brasileiras (CPC / NBC TG):
1. **DRE Oficial Lei 6.404/76**: Demonstração do Resultado do Exercício com segregação precisa entre Receita Bruta, Deduções e Impostos, Custos (CMV/CPV), Despesas Operacionais, EBITDA/LAJIDA e Lucro Líquido.
2. **Plano de Contas Referencial (RFB)**: Cadastro das contas analíticas e sintéticas padrão da Receita Federal para PJ em Geral, Lucro Real, Lucro Presumido e Imunes/Isentas.
3. **Mapeamento Contábil Dinâmico**: De-Para flexível que vincula as contas analíticas do plano societário da empresa às contas da Receita Federal.
4. **SPED Contábil ECD (Escrituração Contábil Digital)**: Geração dos blocos oficiais (0, I, J, 9) com suporte a Livro Diário Geral (Livro G), Livro Diário Resumido (Livro R) com escrituração auxiliar e Livro Razão (Livro B).
5. **Acesso Direto no Desk e na pasta Contabilidade**: Ícone dedicado no Desk e na pasta modal `Accounting`, com menu lateral próprio e atalhos rápidos.

---

## 1. Demonstração do Resultado do Exercício (DRE Lei 6.404/76)

Relatório analítico de alta performance com drill-down direto para os lançamentos de origem:

```
RECEITA OPERACIONAL BRUTA
  (-) Deduções da Receita Bruta (Devoluções, Abatimentos, Descontos Comerciais)
  (-) Tributos Incidentes sobre Vendas (ICMS, PIS, COFINS, ISS)
(=) RECEITA OPERACIONAL LÍQUIDA
  (-) Custos das Mercadorias e Produtos Vendidos (CMV / CPV)
(=) LUCRO BRUTO
  (-) Despesas com Vendas
  (-) Despesas Gerais e Administrativas
  (+/-) Resultado Financeiro Líquido (Receitas Financeiras - Despesas Financeiras)
  (+/-) Outras Receitas e Despesas Operacionais
(=) RESULTADO OPERACIONAL ANTES DO IRPJ/CSLL (EBIT / LAJIR)
  (-) Provisão para IRPJ e Contribuição Social (CSLL)
(=) LUCRO / PREJUÍZO LÍQUIDO DO EXERCÍCIO
```

### Recursos da DRE:
* **Comparativo Mensal e Trimestral**: Visualização em colunas por período selecionado.
* **Análise Vertical (AV %)**: Proporção percentual de cada conta em relação à Receita Bruta ou Receita Líquida.
* **Análise Horizontal (AH %)**: Variação percentual entre períodos consecutivos.
* **Exportação**: Impressão e download em PDF e Excel formatado.

---

## 2. Plano de Contas Referencial e Mapeamento (De-Para)

Para atender as obrigações da ECF e ECD, o módulo disponibiliza:
* **`Plano de Contas Referencial`**: Base pré-carregada das tabelas dinâmicas da Receita Federal (Tabela de Contas da RFB).
* **`Mapeamento Contabil`**: Interface onde cada conta contábil analítica da empresa é associada a uma conta referencial correspondente, com data de início e término de vigência.
* Validação automática para prevenir envio de contas sem mapeamento ao SPED.

---

## 3. SPED Contábil ECD (Escrituração Contábil Digital)

Geração do arquivo digital `.txt` no leiaute do Sistema Público de Escrituração Digital da Receita Federal:
* **Bloco 0**: Abertura, identificação da entidade e parâmetros de escrituração.
* **Bloco I**: Lançamentos contábeis, Livro Diário, Livro Razão, Plano de Contas e Balancetes Diários/Mensais.
* **Bloco J**: Demonstrações Contábeis (Balanço Patrimonial e DRE referencial).
* **Bloco 9**: Encerramento e controle de registros.

---

## 4. Arquitetura e Modelo de Dados

| DocType | Tipo | Finalidade |
| :--- | :--- | :--- |
| **`Configuracao SPED ECD`** | Cadastro | Parametrização da empresa para geração da ECD: qualificação do assinante, indicador do plano de contas, tipo de escrituração (*G, R, B*) e dados do contador (CRC). |
| **`Plano de Contas Referencial`** | Cadastro | Contas contábeis sintéticas e analíticas publicadas pela Receita Federal. |
| **`Mapeamento Contabil`** | Operação | Vínculo De-Para entre a conta contábil do ERPNext e a conta referencial da RFB. |
| **`DRE Lei 6404 76`** | Relatório | Script Report da Demonstração do Resultado com agrupadores societários e análises. |
| **`SPED Contabil ECD`** | Relatório | Gerador e validador do arquivo texto da ECD. |

---

## 5. Estrutura de Diretórios e Código-Fonte

```
erpz_contabil/
├── desktop_icon/
│   └── erpz_contabil.json         # Ícone oficial no Desk e na pasta Accounting
├── erpz_contabil/
│   ├── doctype/
│   │   ├── configuracao_sped_ecd/ # Parâmetros do SPED ECD e dados do contador
│   │   ├── plano_de_contas_referencial/ # Contas oficiais da RFB
│   │   └── mapeamento_contabil/   # De-Para societário vs referencial
│   ├── report/
│   │   ├── dre_lei_6404_76/       # DRE legal societária
│   │   └── sped_contabil_ecd/     # Gerador do arquivo da ECD
│   ├── workspace/
│   │   └── erpz_contabil/         # Workspace contábil com atalhos
│   └── workspace_sidebar/
│       └── erpz_contabil.json     # Menu lateral do ERPZ Contábil
├── hooks.py
├── setup.py                       # Inicialização e vinculações
└── pyproject.toml
```

---

## Licença

Distribuído sob licença MIT. Desenvolvido para o ecossistema ERPZ / Frappe Framework v16.
