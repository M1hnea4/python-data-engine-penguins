from repository import PenguinRepository
from service import PenguinService
from ui import ConsoleUI
from tests import run_tests  

if __name__ == "__main__":
    run_tests()
    repo = PenguinRepository()       
    service = PenguinService(repo)  
    ui = ConsoleUI(service)          
    ui.start()