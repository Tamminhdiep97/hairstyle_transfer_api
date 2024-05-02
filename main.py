import time

from loguru import logger
import config as fc
from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
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
        docs_url=None,
        redoc_url=None
    )
    WORKING_CDN = "unpkg.com"
    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url=f"https://{WORKING_CDN}/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
            swagger_css_url=f"https://{WORKING_CDN}/swagger-ui-dist@5.9.0/swagger-ui.css",
        )


    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()


    @app.get("/redoc", include_in_schema=False)
    async def redoc_html():
        return get_redoc_html(
            openapi_url=app.openapi_url,
            title=app.title + " - ReDoc",
            redoc_js_url=f"https://{WORKING_CDN}/redoc@next/bundles/redoc.standalone.js",
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
    logger.info('Include api router')
    return app


with logger.catch():
    app = app_setting()
