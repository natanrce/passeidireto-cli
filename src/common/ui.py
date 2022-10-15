from os import system

class UI:
  SPINNER_DELAY = 0.1
  
  @staticmethod
  def clear_last_print():
    """Clear the last print
    """
    print('\033[A', end='')
    
  @staticmethod
  def clear_console():
    """Clears the console,
    works on any OS
    """
    system('cls||clear')

  @staticmethod
  def spinner_factory(frames):
    while True:
      for cursor in frames:
        yield cursor
        
  @staticmethod
  def spinner_animate(spinner):
    return '\b' + next(spinner)
