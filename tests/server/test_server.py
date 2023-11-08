# Allow import without error 
# "relative import with no known parent package"
# In vscode, add .env file with PYTHONPATH="..." 
# with the same dir to allow intellisense
import os
import sys
__fileDir__ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
__libdir__ = os.path.dirname(__fileDir__)
sys.path.append(__libdir__)
__srcDir__ = os.path.join(__libdir__ , 'src', 'api')
sys.path.append(__srcDir__)

from dotenv import load_dotenv
load_dotenv()

PLAYER=os.getenv('PLAYER_ID')
ARENA=os.getenv('ARENA')
USERNAME=os.getenv('USERNAME')
PASSWORD=os.getenv('PASSWORD')
SERVER=os.getenv('SERVER')
PORT=int(os.getenv('PORT'))

# Import of main class
from src.api.spythoon import PytactxPainter

def createAgent(playerId):
    return PytactxPainter(playerId=playerId, arena=ARENA, username=USERNAME, password=PASSWORD, server=SERVER, port=PORT)