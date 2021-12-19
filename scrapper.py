import sqlite3
from flask import Flask, flash, jsonify
from flask_restful import Resource, Api

from selenium import webdriver
from selenium.webdriver.common.by import By

app = Flask(__name__)
app.config['SECRET_KEY'] = 'custom secret key'
api = Api(app)

DRIVER_PATH = '/home/raijo/Downloads/chromedriver_linux64/chromedriver'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


class ScrapperClass(Resource):
    
    def get(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get('https://www.indeed.com/viewjob?jk=c13bc626ca6e2bdc')

        company_name = driver.find_element(by=By.CSS_SELECTOR, value=".icl-u-xs-mr--xs").text
        
        company_address = driver.find_element(by=By.XPATH, value="//div[@class='icl-u-xs-mt--xs icl-u-textColor--secondary jobsearch-JobInfoHeader-subtitle jobsearch-DesktopStickyContainer-subtitle']/div[2]").text
        
        job_types = driver.find_element(by=By.CSS_SELECTOR, value=".jobsearch-JobMetadataHeader-item").text
        
        apply_url = driver.find_element(by=By.LINK_TEXT, value="Apply on company site").get_attribute('href')
        
        jk = str(driver.current_url)
        start_ind = jk.index("jk=")
        job_id = jk[start_ind+3:]

        # job_benifits = driver.find_element(by=By.XPATH, value="//div[@class='mosaic mosaic-provider-company-info-salary mosaic-rst mosaic-provider-hydrated']")
        
        driver.quit()
        conn = get_db_connection()

        try:
            conn.execute(
                'INSERT INTO job (job_id, job_types, company_name, benefits, address, apply_url) VALUES (?, ?, ?, ?, ?, ?)',
                (job_id, job_types, company_name, '', company_address, apply_url)
            )
            conn.commit()
        except:
            conn.rollback()

        job = conn.execute(
            'SELECT * FROM job'
        ).fetchone()

        conn.close()

        return jsonify({
            "job_id": job['job_id'],
            "job_types": job['job_types'],
            "company_name": job['company_name'],
            "benefits": job['benefits'],
            "address": job['address'],
            "apply_url": job['apply_url']
            })

api.add_resource(ScrapperClass, '/job-scrapper')

if __name__ == '__main__':
    app.run(debug=True)
