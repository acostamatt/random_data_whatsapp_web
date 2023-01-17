import threading
import time

from controllers.sorteo import SorteoController

sorteo = SorteoController()
sorteo.init_thread()
