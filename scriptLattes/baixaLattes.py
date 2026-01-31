#!/usr/bin/python
# encoding: utf-8

import argparse
import time
import os
import urllib.request, urllib.parse, urllib.error
import platform
import warnings
import re

try:
    import bs4
except ImportError:
    bs4 = None

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
except ImportError:
    sync_playwright = None
    PlaywrightTimeoutError = None

import platform
import warnings
warnings.filterwarnings("ignore")

RESULTS_DIR = os.environ.get('DATA_DIR', 'htmls')
URL = 'http://buscatextual.cnpq.br/buscatextual/preview.do?metodo=apresentar&id={0}'
URL_LATTES_ID10 = 'http://buscatextual.cnpq.br/buscatextual/visualizacv.do?id={0}'
URL_LATTES_ID16 = 'http://lattes.cnpq.br/{0}'


class LattesRobot:
    def __init__(self, results_dir):
        """
        Initialize the LattesRobot with Playwright.
        
        Args:
            results_dir: Directory to save downloaded CV HTML files
        """
        self.results_dir = results_dir
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.identifiers = set()
        self.downloaded_identifiers = set()
        self.lid_type = -1
        self.initialize()

    def initialize(self):
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)

    def load_codes(self, id_lattes):
        self.identifiers.add(id_lattes)
        self._set_lid_type()

    def check_downloaded_cvs(self):
        self.downloaded_identifiers = {h for h in os.listdir(self.results_dir) if len(h) == self.lid_type}

    def create_browser(self):
        """Create and configure the Playwright browser instance."""
        if sync_playwright is None:
            raise ImportError("Playwright is not installed. Run: pip install playwright && playwright install chromium")
        
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
            ]
        )
        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            java_script_enabled=True,
        )
        self.page = self.context.new_page()

    def collect_html_cvs(self, start, end):
        total_lids = len(list(self.identifiers)[start:end])

        for identifier in sorted(self.identifiers)[start:end]:
            lids = self._get_lids_10_16(identifier)

            if lids[10]:
                if lids[self.lid_type] not in self.downloaded_identifiers:
                    self._execute_js(lids)

    def store_html(self, lid, page_content):
        with open(os.path.join(self.results_dir, lid), 'wb') as fout:
            try:
                data = page_content.encode('utf-8', 'replace').strip()
            except UnicodeEncodeError:
                data = page_content.encode('utf-8').strip()

            if data:
                fout.write(data)
        
    def _execute_js(self, lids):
        self.page.goto(URL.format(lids[10]), wait_until='networkidle')

        cmd_open_cv = 'abreCV()'
        self.page.evaluate(cmd_open_cv)
        
        # Wait for new page/popup to open
        self.page.wait_for_timeout(2000)
        
        # Get the last page in context (new window)
        pages = self.context.pages
        if len(pages) > 1:
            self.page = pages[-1]
            self.page.wait_for_load_state('networkidle')

        if not lids[16]:
            page_content = self.page.content()
            lids[16] = self._extract_lid16(page_content)

            if self.lid_type == 16 and len(lids[16]) != 16:
                return

        self.store_html(lids[self.lid_type], self.page.content())

    def _get_lids_10_16(self, lid):
        lids = {10: '', 16: ''}

        if len(lid) == 10:
            lids[10] = lid

        if len(lid) == 16:
            lids[16] = lid

            self.page.goto(URL_LATTES_ID16.format(lid), wait_until='networkidle')
            current_url = self.page.url
            parsed = urllib.parse.urlparse(current_url)
            query_params = urllib.parse.parse_qs(parsed.query)
            if 'id' in query_params:
                lid10 = query_params['id'][0]
                if len(lid10) == 10:
                    lids[10] = lid10

        return lids

    def _extract_lid16(self, page_source):
        if bs4:
            soup = bs4.BeautifulSoup(page_source, 'html.parser')
            span = soup.find('span', attrs={'style': 'font-weight: bold; color: #326C99;'})
            if span:
                lid16 = span.text.encode()
            else:
                return None
        else:
            match = re.search(r'<span style="font-weight: bold; color: #326C99;">(.*?)</span>', page_source)
            if match:
                lid16 = match.group(1).encode()
            else:
                return None

        if len(lid16) == 16 and lid16.isdigit():
            return lid16

    def _set_lid_type(self):
        if len(self.identifiers) > 0:
            ld = len(list(self.identifiers)[0])
            self.lid_type = ld

    def close(self):
        """Clean up Playwright resources."""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()


def __get_data(id_lattes, diretorio):
    rob = LattesRobot(results_dir=diretorio)
    print(f"Baixando CV Lattes: {id_lattes}. Este processo pode demorar alguns segundos.")
    rob.load_codes(id_lattes)
    rob.check_downloaded_cvs()
    rob.create_browser()

    try:
        rob.collect_html_cvs(0, None)
    finally:
        rob.close()


def baixaCVLattes(id_lattes, diretorio):
    """
    Download a Lattes CV by its identifier.
    
    Args:
        id_lattes: The Lattes identifier (10 or 16 digits)
        diretorio: Directory to save the downloaded HTML file
        
    Raises:
        Exception: If download fails after 5 attempts
    """
    max_tentativas = 5
    tentativas = 0

    while tentativas < max_tentativas:
        destino = os.path.join(diretorio, id_lattes)
        if os.path.exists(destino):
            return

        try:
            __get_data(id_lattes, diretorio)
        except PlaywrightTimeoutError as e:
            print(f"Timeout ao baixar {id_lattes}: dormindo 5 minutos antes de tentar novamente...")
            time.sleep(300)  # 5 minutos
            print(f"Retomando tentativa de download do CV Lattes: {id_lattes}")
            continue
        except Exception as e:
            if 'ERR_CONNECTION_REFUSED' in str(e):
                print(f"Connection refused ao baixar {id_lattes}: dormindo 5 minutos antes de tentar novamente...")
                time.sleep(300)  # 5 minutos
                print(f"Retomando tentativa de download do CV Lattes: {id_lattes}")
                continue
            else:
                raise

        destino = os.path.join(diretorio, id_lattes)
        if os.path.exists(destino):
            return
        else:
            tentativas += 1
            print(f"Tentativa #{tentativas} falhou para {id_lattes}. Restam {max_tentativas - tentativas} tentativas.")

    raise Exception(f"Não foi possível baixar o CV Lattes de {id_lattes} após {max_tentativas} tentativas.")
