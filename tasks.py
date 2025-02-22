from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP 
from RPA.Excel.Files import Files
from RPA.PDF import PDF


@task
def robot_spare_bin_python():
    """Enter sales data for the week and export it to PDF"""
    browser.configure(
        slowmo= 10,
    )
    open_the_intranet_website()
    log_in()
    download_excel_file()
    fill_form_with_excel_data()
    collect_results()
    log_out()
    export_to_pdf()





def open_the_intranet_website():
    """Open the intranet website"""
    browser.goto("https://robotsparebinindustries.com/")

def log_in():
    """"Log in to the intranet"""
    page = browser.page()
    page.fill("#username", "maria")
    page.fill("#password", "thoushallnotpass")
    page.click("button:text('Log in')")

def download_excel_file():
    """Download the Excel file"""
    http = HTTP()
    http.download(url="https://robotsparebinindustries.com/SalesData.xlsx",  
                  overwrite=True)
    
def fill_form_with_excel_data():
    """Fill the form with data from the Excel file"""
    excel = Files()
    excel.open_workbook("SalesData.xlsx")
    worksheet = excel.read_worksheet_as_table("data", header=True)
    excel.close_workbook()

    for row in worksheet:
        fill_and_submit_the_form(row)

def fill_and_submit_the_form(sales_rep):
    """Fill and submit the form"""
    page = browser.page()
    page.fill("#firstname",sales_rep["First Name"])
    page.fill("#lastname", sales_rep["Last Name"])
    page.select_option("#salestarget", str(sales_rep["Sales Target"]))
    page.fill("#salesresult", str(sales_rep["Sales"]))
    page.click("text = Submit")

def collect_results():
    """Take a screenshot of the results"""
    page = browser.page()
    page.screenshot(path = "output/sales_summary.png")

def log_out():
    """Log out from the intranet"""
    page = browser.page()
    page.click("text = Log out")

def export_to_pdf():
    """Export the results to PDF"""
    page = browser.page()
    sales_results_html = page.locator("sales-results").inner_html()

    pdf = PDF()
    pdf.html_to_pdf(sales_results_html, "output/sales_results.pdf")
