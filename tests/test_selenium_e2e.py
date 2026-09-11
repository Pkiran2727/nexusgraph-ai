import os
import sys
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class TestNexusGraphSeleniumE2E(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        try:
            cls.driver = webdriver.Chrome(options=chrome_options)
            cls.driver.implicitly_wait(10)
        except Exception as e:
            print(f"[Selenium Note] ChromeDriver initialization note: {e}")
            cls.driver = None

    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            cls.driver.quit()

    def test_01_homepage_and_stat_cards(self):
        if not self.driver:
            self.skipTest("Selenium WebDriver not initialized in headless environment.")

        self.driver.get("http://localhost:8095/")
        time.sleep(2)

        # Check title
        self.assertIn("NexusGraph AI", self.driver.title)

        # Check header logo
        header_title = self.driver.find_element(By.TAG_NAME, "h1").text
        self.assertEqual(header_title, "NexusGraph AI")

        # Check stats cards
        proc_stat = self.driver.find_element(By.ID, "stat-processes").text
        self.assertGreater(int(proc_stat), 0)

    def test_02_tab_navigation_and_role_analytics(self):
        if not self.driver:
            self.skipTest("Selenium WebDriver not initialized in headless environment.")

        self.driver.get("http://localhost:8095/")
        time.sleep(2)

        # Click Tab 2 (Role AI Impact Analyzer)
        tab_btn = self.driver.find_element(By.XPATH, "//button[@data-tab='tab-role']")
        tab_btn.click()
        time.sleep(1)

        # Click Analyze Role button
        analyze_btn = self.driver.find_element(By.ID, "btn-analyze-role")
        analyze_btn.click()
        time.sleep(2)

        # Check role results updated
        results_area = self.driver.find_element(By.ID, "role-analysis-results").text
        self.assertIn("AI EXPOSURE INDEX", results_area)

    def test_03_surprise_record_ingestion_form(self):
        if not self.driver:
            self.skipTest("Selenium WebDriver not initialized in headless environment.")

        self.driver.get("http://localhost:8095/")
        time.sleep(2)

        # Click Tab 4 (Live Surprise Record Test)
        tab_btn = self.driver.find_element(By.XPATH, "//button[@data-tab='tab-surprise']")
        tab_btn.click()
        time.sleep(1)

        # Input surprise record
        name_field = self.driver.find_element(By.ID, "surprise-name")
        name_field.send_keys("Automated Warehouse Drone Fleet")

        ingest_btn = self.driver.find_element(By.ID, "btn-ingest-surprise")
        ingest_btn.click()
        time.sleep(3)

        # Check audit log output
        results_area = self.driver.find_element(By.ID, "surprise-results").text
        self.assertIn("Ingestion Successful", results_area)

if __name__ == "__main__":
    unittest.main()
