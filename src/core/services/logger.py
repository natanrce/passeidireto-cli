from time import sleep
from common.ui import UI

class Logger:
  RED="\033[38;5;9m"
  CYAN="\033[38;5;45m"
  DEFAULT="\033[0m"
  
  def __init__(self, ctx) -> None:
    self.context = ctx
    
  def log(self, message):
    print(message)
    
  def warn(self, msg) -> None:
    print(f'{self.RED}[-]{self.DEFAULT} {msg}')
    
  def info(self, message):
    print(f'{self.CYAN}[*]{self.DEFAULT} {message}')
  
  def animated_info(self, message):
    spinner = UI.spinner_factory('|/-\\')
    info_message = f'{self.CYAN}[*]{self.DEFAULT} {message}'
    
    print() # New line
    
    for i in range(len(info_message)):
      UI.clear_last_print()
      current_msg = info_message[:i] + info_message[i:].capitalize()
      
      print(
        current_msg,
        UI.spinner_animate(spinner)
      )
      
      sleep(UI.SPINNER_DELAY)