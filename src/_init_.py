from src.WandSim.WandSimulatorManager import startSimulator
import time

start = time.time()
print("Begin", start)

startSimulator()

end = time.time()
print("End time ", end, "Elapsed time", end - start)
