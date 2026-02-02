import subprocess
import sys
import time
from os import path

CONTROLLER_SCRIPT = path.join('HandTracker','tracker.py')
GAME_SCRIPT = path.join('Tetris','TetrisGame.py')

print('Launching controller....')
controller = subprocess.Popen([sys.executable, CONTROLLER_SCRIPT])

time.sleep(2)

print("Opnening Game...")
game = subprocess.Popen([sys.executable, GAME_SCRIPT])

try:

    while True:
        controller_status = controller.poll()
        game_status = game.poll()

        if game_status is not None or controller_status is not None:
            print('A process has teriminated')
            break

        time.sleep(1)


except KeyboardInterrupt:
    print('Closing')

print('Shutting down')
controller.terminate()
game.terminate()