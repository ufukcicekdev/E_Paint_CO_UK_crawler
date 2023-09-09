from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import os
import pandas as pd
import logging



logging.basicConfig(filename='paint_uk.log', level=logging.DEBUG)


def open_browser(domain_link):
    with sync_playwright() as playwright:
        chromium = playwright.firefox  # or "firefox" or "webkit".
        browser = chromium.launch(headless=False)
        context = browser.new_context(
            ignore_https_errors=True, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36")
        page = context.new_page()
        page.goto(domain_link)
        page.wait_for_load_state()
        page.wait_for_timeout(5000)
        page_content = page.content()
        soup = BeautifulSoup(page_content, 'html.parser')

        print("Giriş Başarılı!")
        operation(page,soup)


material = []

def operation(page,soup):

    choose_ranges = page.locator("div.lab_values form:nth-child(1) select")
    choose_option_elements = choose_ranges.locator("option").all()
    for element in choose_option_elements[3:]:
        check_element = element.get_attribute("value")
        if check_element != None:
            choose_option_element_option_text = element.inner_text()
            choose_ranges.select_option(choose_option_element_option_text)
            page.wait_for_timeout(5000)
            choose_colour = page.locator("div.lab_values form:nth-child(2) select")
            choose_colour_option_elements = choose_colour.locator("option").all()
            for choose_colour_element in choose_colour_option_elements:
                check_choose_colour_element = choose_colour_element.get_attribute("value")
                if  check_choose_colour_element != None:
                    choose_colour_element_colour_text = choose_colour_element.inner_text()
                    choose_colour.select_option(choose_colour_element_colour_text)
                    page.wait_for_timeout(3000)
                    try:
                        referance =  check_element_selector(page,"#main_body > div > div.right.right-col > div.g-box-w > div.g-box-w.lab-result > span:nth-child(2) > h2:nth-child(1)")
                        colour_name = check_element_selector(page ,"#main_body > div > div.right.right-col > div.g-box-w > div.g-box-w.lab-result > span:nth-child(2) > h3")
                        cmyk_code = check_element_selector(page ,"#main_body > div > div.right.right-col > div.g-box-w > div.g-box-w.lab-result > span:nth-child(4) > div:nth-child(3) > p:nth-child(1) ")
                        sRGB_code = check_element_selector(page ,"#main_body > div > div.right.right-col > div.g-box-w > div.g-box-w.lab-result > span:nth-child(4) > div:nth-child(3) > p:nth-child(2)")
                        hex_code = check_element_selector(page ,"#main_body > div > div.right.right-col > div.g-box-w > div.g-box-w.lab-result > span:nth-child(4) > div:nth-child(3) > p:nth-child(4)")
                        l_code = check_element_selector(page ,"#main_body > div > div.right.right-col > div.g-box-w > div.g-box-w.lab-result > span:nth-child(4) > div:nth-child(1) > div:nth-child(1) > p")
                        a_code = check_element_selector(page ,"#main_body > div > div.right.right-col > div.g-box-w > div.g-box-w.lab-result > span:nth-child(4) > div:nth-child(1) > div:nth-child(2) > p")
                        b_code = check_element_selector(page ,"#main_body > div > div.right.right-col > div.g-box-w > div.g-box-w.lab-result > span:nth-child(4) > div:nth-child(1) > div:nth-child(3) > p")
                        h_code = check_element_selector(page ,"#main_body > div > div.right.right-col > div.g-box-w > div.g-box-w.lab-result > span:nth-child(4) > div:nth-child(2) > div:nth-child(1) > p")
                        l_code2 = check_element_selector(page ,"#main_body > div > div.right.right-col > div.g-box-w > div.g-box-w.lab-result > span:nth-child(4) > div:nth-child(2) > div:nth-child(2) > p")
                        c_code = check_element_selector(page ,"#main_body > div > div.right.right-col > div.g-box-w > div.g-box-w.lab-result > span:nth-child(4) > div:nth-child(2) > div:nth-child(3) > p")

                        print(f"Result: {referance}, {colour_name}, {cmyk_code}, {sRGB_code}, {hex_code}, {l_code}, {a_code}, {b_code}, {h_code}, {l_code2}, {c_code}")
                        mat ={
                            "Range":choose_option_element_option_text,
                            "Referance":referance,
                            "Name": colour_name,
                            "CMYK":cmyk_code.split(":")[1],
                            "sRGB_code":sRGB_code.split(":")[1],
                            "Hex":hex_code.split(":")[1],
                            "L_Code":l_code,
                            "A_Code":a_code,
                            "B_Code":b_code,
                            "H_Code":h_code,
                            "L_Code2":l_code2,
                            "C_Code":c_code,
                        }

                        material.append(mat)
                    except Exception as e:
                        logging.error(f"Failed to {e}")
                        print("Failed to",e)

            df = pd.DataFrame(material)
            print(df.head())
            df.to_excel(f'{choose_option_element_option_text.replace(" ","")}.xlsx')
            material.clear()




def check_element_selector(page,selector):
    try:
        result = page.locator(selector).inner_text()
    except Exception as e:
        logging.error(f"Failed to {e}")
        result =""
    
    return result



if __name__ == "__main__":
    url_list = ["https://www.e-paint.co.uk/lab-hlc-rgb-lrv-values.asp"]
    for url in url_list:
        open_browser(url)

