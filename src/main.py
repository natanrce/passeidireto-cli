def get_args():
  """Get arguments from command line
  """
  from argparse import ArgumentParser
  
  parser = ArgumentParser(
    description='Download any file from passeidireto.com',
    usage='python3 main.py [-h HELP] [-u URL] [-o OUTPUT]'
  )
  
  parser.add_argument('-u', '--url', help='URL of the file to download', required=True)
  parser.add_argument('-o', '--output', help='Filename to save data (.pdf)', required=True)
  
  return parser.parse_args()

if __name__  == '__main__':
  """Main entry point
  """
  from core.app import App
  from core.services.pdf import PdfService
  
  app = App(
    get_args(),
    PdfService()
  )
  app.run()
