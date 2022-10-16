import asyncio

from core.services.pdf import PdfService
from core.services.passeidireto import PasseiDiretoService

from aiohttp.client import ClientSession, TCPConnector

class App:
  def __init__(
    self, 
    args, 
    pdf_service: PdfService,
    passei_direto_service: PasseiDiretoService,
  ):
    self.url = args.url
    self.output_name = args.output
  
    # Dependency injection
    self.pdf_service = pdf_service
    self.passei_direto_service = passei_direto_service
    
  def run(self):
    """Runs the application
    """
    asyncio.run(self.download_material())
  
  async def download_material(self):
    """Downloads all pages from material
    """
    conn = TCPConnector(limit=10)
    
    async with ClientSession(connector=conn) as session:
      tasks = []
      
      fingerprint = await self.passei_direto_service.get_fingerprint(session, self.url)
      
      file_url = fingerprint['FileUrl']
      page_count = fingerprint['FileMetadata']['PreviewPageCount']
      
      for page in range(1, page_count + 1):
        html_content = self.passei_direto_service.get_html(
          session,
          file_url,
          page
        )
        
        task = asyncio.ensure_future(html_content)
        tasks.append(task)
        
      """Callback to apply styles to HTML
      """
      def callback(x):
        return self.passei_direto_service.get_css(x, file_url)
        
      result = await asyncio.gather(*tasks, return_exceptions=True)
      styled_content = list(map(callback, result))
      
      pages_buffer = self.pdf_service.get_all_pages_buffer(styled_content)
      
      self.pdf_service.merge_pdf_and_save(
        pages_buffer,
        self.output_name
      )
