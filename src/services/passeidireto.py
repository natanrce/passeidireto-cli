class PasseiDiretoService:
  async def get_fingerprint(self, session, material_url):
    """Get material information from API
    """
    from re import findall
    
    id = findall(r'\d+', material_url)[0]
    url = 'https://material-api.passeidireto.com/materials/' + id
    
    async with session.get(url) as response:
      data = await response.json()
      return data['SpecificDetails']['FileFingerprint']

  
  async def get_html(self, session, file_url, page_number):
    """Download current material page
    """
    url = f'https://files.passeidireto.com/{file_url}/{page_number}.html'
    
    async with session.get(url) as response:
      return await response.text()
    
  def get_css(self, html_content, file_url):
    """Get and apply styles from material
    """
    from bs4 import BeautifulSoup
    
    url = f'https://files.passeidireto.com/{file_url}/{file_url}.css'
    soup = BeautifulSoup(html_content, features='html5lib')
    
    style_links = [
      { 'rel': 'stylesheet', 'href': url },
      { 'rel': 'stylesheet', 'href': './styles/style.css' },
    ]
    
    body_children = [
      { 'id': 'file-viewer' },
      { 'class': 'document-viewer' },
      { 'class': 'document-section' },
      { 'class': 'document-fragment' },
      { 'class': 'page-container' },
      { 'class': 'page-content' },
    ]

    for link in style_links:
      new_tag = soup.new_tag('link', **link)
      soup.head.append(new_tag)
    
    body_div = soup.body
    content_div = soup.body.div

    for child in body_children:
      div = soup.new_tag('div', **child)
      body_div.append(div)

      body_div = div

    body_div.insert(0, content_div)

    return str(soup)