import cv2
from loguru import logger
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import Response
from starlette.requests import Request
import numpy as np
import aiofiles

from hairstyle_transfer_tool import Tool
import config as cf
import utils


api_router = APIRouter()
tool = Tool(opts=None, result_path=cf.result_path, checkpoint_path='./best_model.pt')


def load_image_into_numpy_array(data):
    npimg = np.frombuffer(data, np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    frame_convert = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame_convert


@api_router.get('/collect_info/')
async def welcome():
    result_dict = dict()
    logger.info(utils.dict_from_module(cf))
    result_dict['Config'] = utils.dict_from_module(cf)
    result_dict['Message'] = 'Welcome to Hairstyle Transfer API-System'
    return result_dict


@api_router.post(
    '/infer/transfer/',
    responses={
        200: {"content": {"image/png": {}}}
    },
)
async def transfer_hair(
    #request: Request,
        source: UploadFile = File(...),
        target: UploadFile = File(...)
    ):
    """transfer hair from target to source face.

    - file: image file contain face
    """
    image_files = []
    for file_ in [source, target]:
        try:
            contents = await file_.read()
            # async with aiofiles.open(file_.filename, 'wb') as f:
            #     await f.write(contents)
        except Exception:
            return {"message": "There was an error uploading the file"}
        finally:
            file_.file.close()
            image_files.append(load_image_into_numpy_array(contents))
    result_image = cv2.cvtColor(
            tool.hairstyle_transfer_api(image_files[0], image_files[1]),
            cv2.COLOR_RGB2BGR
    )
    result_encoded = cv2.imencode(".png", result_image)[1].tobytes()
    return Response(content=result_encoded, media_type="image/png")

