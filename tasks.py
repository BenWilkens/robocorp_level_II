from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Tables import Tables

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
    # fill_the_form()


def open_robot_order_website():
    # TODO: Implement your function here
    """Open robot order web portal"""
    browser.goto("https://robotsparebinindustries.com/#/robot-order") 
    page = browser.page()
    page.wait_for_load_state()
    close_annoying_modal()
    page.screenshot(path="screenshots/page_load.png", full_page=True)
    

def download_order_file():
    """Downloads excel file from the given URL"""
    http = HTTP()
    http.download(url="https://robotsparebinindustries.com/orders.csv", overwrite=True)


def get_orders():
    # Function code here
    library = Tables()
    orders = library.read_table_from_csv(
        "orders.csv", columns=["Order","number","Head","Body","Legs","Address"]
    )
    return orders

def fill_the_form(order):
    page = browser.page()
    
    # Order number,Head,Body,Legs,Address
    # Choose Head from dropdown
    
    # Click Body radion button
    # Enter legs
    page.fill("xpath=/html/body/div[1]/div/div[1]/div/div[1]/form/div[3]/input", order['Legs'])
    # Enter shipping address
    page.fill("xpath=/html/body/div[1]/div/div[1]/div/div[1]/form/div[4]/inputt", order['Address'])
    page.screenshot(path="sreenshots/order_"+order['Order'])


def close_annoying_modal():
    page = browser.page()
    page.click("button:text('OK')")

def loop_and_process_orders():
    orders = get_orders()
    for order in orders:
        fill_the_form(order)

        print(order)


"""
from RPA.Tables import Tables

library = Tables()
orders = library.read_table_from_csv(
    "orders.csv", columns=["name", "mail", "product"]
)

customers = library.group_table_by_column(rows, "mail")
for customer in customers:
    for order in customer:
        add_cart(order)
    make_order()
"""