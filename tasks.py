from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
from RPA.Archive import Archive


@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    open_robot_order_website()
    download_order_file()
    loop_and_process_orders()
    archive_receipts()
    # fill_the_form()


def open_robot_order_website():
    # TODO: Implement your function here
    """Open robot order web portal"""
    browser.goto("https://robotsparebinindustries.com/#/robot-order") 
    page = browser.page()
    page.wait_for_load_state()
    close_annoying_modal()
    page.screenshot(path="outputs/screenshots/page_load.png", full_page=True)
    

def download_order_file():
    """Downloads excel file from the given URL"""
    http = HTTP()
    http.download(url="https://robotsparebinindustries.com/orders.csv", overwrite=True)


def get_orders():
    # Function code here
    library = Tables()
    orders = library.read_table_from_csv(
        "orders.csv", columns=["Order number","Head","Body","Legs","Address"]
    )
    return orders

def fill_the_form(order):
    page = browser.page()
    heads = {
    "1" : "Roll-a-thor head",
    "2" : "Peanut crusher head",
    "3" : "D.A.V.E head",
    "4" : "Andy Roid head",
    "5" : "Spanner mate head",
    "6" : "Drillbit 2000 head"
    }
    head = order["Head"]
    page.select_option("#head", heads.get(head))
    # Order number,Head,Body,Legs,Address
    
    # Choose Head from dropdown
    heads = {
    "1" : "Roll-a-thor head",
    "2" : "Peanut crusher head",
    "3" : "D.A.V.E head",
    "4" : "Andy Roid head",
    "5" : "Spanner mate head",
    "6" : "Drillbit 2000 head"
    }
    head = order["Head"]
    page.select_option("#head", heads.get(head))
    
    # Click Body radion button
    # default to 0 but replace using formatted string with Body option from each order
    page.click('//*[@id="root"]/div/div[1]/div/div[1]/form/div[2]/div/div[{0}]/label'.format(order["Body"]))
    
    # Enter legs
    # page.fill("input[placeholder='Enter the part number for the legs']", order['Legs'])
    page.fill("input[placeholder='Enter the part number for the legs']", order["Legs"])

    # Enter shipping address
    page.fill("xpath=/html/body/div[1]/div/div[1]/div/div[1]/form/div[4]/input", order['Address'])
    


def close_annoying_modal():
    page = browser.page()
    page.click("button:text('OK')")

def loop_and_process_orders():
    page = browser.page()
    orders = get_orders()
    for order in orders:
        fill_the_form(order)
        # take a screenshot of the preview
        page.click("button:text('Preview')")
        page.wait_for_selector(selector="#robot-preview-image")
        
        # Submit order
        error_occured = True

        while error_occured:
            page.click("button:text('Order')")
            error_occured = page.locator("//div[@class= 'alert alert-danger']").is_visible()
            if not error_occured:
                break
        
        # save PDF of receipt
        store_receipt_as_pdf(order["Order number"])
        page.click("#order-another")
        close_annoying_modal()


def store_receipt_as_pdf(order_number):
    """Store each receipt as a PDf"""
    page = browser.page()
    receipt_html = page.locator("#receipt").inner_html()
    pdf = PDF()
    receipt_path = "output/receipts/order_{0}.pdf".format(order_number)
    pdf.html_to_pdf(receipt_html, receipt_path)
    # Embed screenshot in each PDF
    screenshot_robot_preview(order_number)
    embed_screenshot_in_receipt_pdf("output/screenshots/order_"+order_number+".png", receipt_path)




def screenshot_robot_preview(order_number):
    """Screenshot the robot preview"""
    page = browser.page()
    page.locator(selector="#robot-preview-image").screenshot(path="output/screenshots/order_"+order_number+".png")


def embed_screenshot_in_receipt_pdf(screenshot, receipt):
    pdf = PDF()
    pdf.add_files_to_pdf( files=[screenshot], target_document=receipt, append=True)


def archive_receipts():
    """Create Zip Archive of all reciepts"""
    lib = Archive()
    lib.archive_folder_with_zip("output/receipts","receipts.zip",recursive=True)