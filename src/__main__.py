"""
Entry point

"""
import uvicorn

from calendar_back import APP, LOGGER, API_PORT, API_IP, LOG_CONFIG

# for vercel deployment
app = APP 

if __name__ == '__main__':
    LOGGER.debug("Starting...")
    uvicorn.run(
        APP,
        host=API_IP,
        port=API_PORT,
        reload=False,
        log_config=LOG_CONFIG
    )
    LOGGER.debug("Ending.")
