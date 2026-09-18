app_name = "erpz_contabil"
app_title = "ERPZ Contábil"
app_publisher = "ERPZ"
app_description = "Demonstrações Cont?beis Brasileiras (DRE 6.404/76, Balan?o), Mapeamento RFB e SPED ECD"
app_email = "dev@erpz.io"
app_license = "mit"
app_version = "0.0.1"

required_apps = ["frappe", "erpnext"]

after_install = 'erpz_contabil.setup.after_install'
after_migrate = 'erpz_contabil.setup.after_migrate'
