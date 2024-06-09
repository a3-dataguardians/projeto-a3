import scrapy
import os

class SspSpSpider(scrapy.Spider):
    name = 'ssp_sp'
    allowed_domains = ['ssp.sp.gov.br']
    start_urls = ['https://www.ssp.sp.gov.br/estatistica/dados-mensais']

    def parse(self, response):
        # Selecionar os links dos arquivos de dados
        for link in response.css('a::attr(href)').extract():
            if "estatistica" in link and link.endswith(".csv"):
                yield response.follow(link, self.download_data)

    def download_data(self, response):
        # Extrair o nome do arquivo a partir da URL
        path = response.url.split('/')[-1]
        # Criar um diretório para salvar os arquivos, se não existir
        if not os.path.exists('data'):
            os.makedirs('data')
        # Caminho completo do arquivo
        full_path = os.path.join('data', path)
        self.log(f'Saving file {full_path}')
        # Salvar o conteúdo do arquivo
        with open(full_path, 'wb') as f:
            f.write(response.body)
