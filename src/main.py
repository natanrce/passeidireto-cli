from services.passeidireto import PasseiDiretoService

def get_args():
  """Get arguments from command line
  """
  from argparse import ArgumentParser
  
  parser = ArgumentParser(
    description='Download any file from passeidireto.com',
    usage='python3 main.py [-h HELP] [-u URL] [-o OUTPUT]'
  )
  
  parser.add_argument('-u', '--url', help='Material url to download', required=True)
  parser.add_argument('-o', '--output', help='Output filename', required=True)
  
  return parser.parse_args()

if __name__  == '__main__':
  """Main entry point
  """
  from app import App
  from services.pdf import PdfService
  
  app = App(
    get_args(),
    PdfService(),
    PasseiDiretoService()
  )
  app.run()
