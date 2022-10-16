from os import system

class UI:
  @staticmethod
  def clear_console():
    """Clears the console,
    works on any OS
    """
    system('cls||clear')
