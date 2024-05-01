import time

from loguru import logger
import config as fc
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from handler import api_router
import log as fulog


def app_setting():
    # log setting
    time_stamp = time.strftime('%Y_%m_%d_%H%M%S', time.localtime())
    log_file_path = 'logs/app_{}.log'.format(time_stamp)
    logger = fulog.setup_logger(
        log_file_path=log_file_path,
        level=fc.LOG_LEVEL,
        rotation=fc.ROTATION,
        retention=fc.RETENTION,
    )

    logger.info('Init the API SERVER')

    app = FastAPI(
        title=fc.APP_NAME,
        version=fc.API_VERSION,
        description=fc.API_DESCRIPTION,
        debug=fc.DEBUG,
    )

    logger.info('Started API SERVER')

    # setting logger
    app.logger = logger

    # add middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    # setting router
    app.include_router(api_router, prefix=fc.API_PREFIX)
    return app


with logger.catch():
    app = app_setting()
