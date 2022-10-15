import re
import asyncio

from bs4 import BeautifulSoup
from core.services.pdf import PdfService
from aiohttp.client import ClientSession, TCPConnector

class App:
  def __init__(self, args, pdf_service: PdfService):
    self.pdf_service = pdf_service
    
    self.url = args.url
    self.output_name = args.output
  
  def run(self):
    """Runs the application
    """
    asyncio.run(self.download_all())
  
  async def download_all(self):
    """Downloads all pages from material
    """
    conn = TCPConnector(limit=10)
    material_id = re.findall(r'\d+', self.url)[0]
    
    async with ClientSession(connector=conn) as session:
      tasks = []
      
      fingerprint = await self.get_material_fingerprint(session, material_id)
      
      file_url = fingerprint['FileUrl']
      page_count = fingerprint['FileMetadata']['PreviewPageCount']
      
      for page in range(1, page_count + 1):
        task = asyncio.ensure_future(
          self.get_html(session, file_url, page)
        )
        
        tasks.append(task)
        
      """Callback to apply styles (CSS) to HTML
      """
      def callback(x):
        return self.get_css(x, file_url)
        
      result = await asyncio.gather(*tasks, return_exceptions=True)
      styled_content = [x for x in map(callback, result)]
      
      self.pdf_service.merge_pdf_and_save(
        self.pdf_service.get_all_pages_buffer(styled_content),
        self.output_name
      )
            
  async def get_html(self, session, file_url, page_number):
    """Download current material page
    """
    url = f'https://files.passeidireto.com/{file_url}/{page_number}.html'
    
    async with session.get(url) as response:
      return await response.text()
   
  def get_css(self, html_content, file_url):
    """Get and apply styles from material
    """
    url = f'https://files.passeidireto.com/{file_url}/{file_url}.css'
    soup = BeautifulSoup(html_content, features='html5lib')
    
    style_links = [
      { 'tag': 'link', 'rel': 'stylesheet', 'href': 'src/common/styles/style.css' },
      { 'tag': 'link', 'rel': 'stylesheet', 'href': url },
    ]
    
    for link in style_links:
      new_tag = soup.new_tag(link['tag'], **link)
      soup.head.append(new_tag)
    
    return str(soup)
    
  async def get_material_fingerprint(self, session, material_id):
    """Get material information from API
    """
    url = 'https://material-api.passeidireto.com/materials/' + material_id
    
    async with session.get(url) as response:
      data = await response.json()
      return data['SpecificDetails']['FileFingerprint']
