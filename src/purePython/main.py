from utils.config import Definitions
from utils.logger import LogSetup
from controllers.sync_controller import WakeUp
from controllers.async_controller import AsyncWakeUp
import logging
import debugpy

def run():
    logger = LogSetup()
    config = Definitions()
    controller = AsyncWakeUp() if config.ASYNC_MODE else WakeUp()
    
    logger.enableLog(config.LOG_DIR, config.LOG_FILE_NAME)
    
    if config.DEBUG_MODE:
        logging.info("Running debugpy.listen()")
        debugpy.listen(("0.0.0.0", config.DEBUG_PORT))
        logging.info("Waiting for debugger attach...")
        debugpy.wait_for_client()  # Optional: pause until debugger connects
    
    msg = "Asynchronous controller ON" if config.ASYNC_MODE else "Synchronous controller ON"
    logging.info(msg)
    controller.startup_routine()

if __name__ == "__main__":
    run()