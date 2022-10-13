import os
import queue
from threading import Thread
from utils.frame_extractor import FrameExtractor

from model_providers.maniqa.model_inferencer import Inferencer
from loaders.uploader import Uploader
from loaders.downloader import YoutubeDownloader
from model_providers.maniqa.model_provider import ModelProvider
from schemas.schema_request import Request
#from services.request_service import get_all_requests, delete_request
from services.service_binder import get_db


class ManiqaInteractor():

    TYPE = "maniqa"
    queue = queue.SimpleQueue()

    def __init__(self, model_inferencer: Inferencer, uploader: Uploader, downloader: YoutubeDownloader) -> None:
        self.model_inferencer = model_inferencer
        self.preview_uploader = uploader
        self.downloader = downloader
        self.daemon = Thread(target=self.__invoke, daemon=True, name='Maniqa')
        self.is_started = False
        self.__start()
    

    def __invoke(self):
        while not self.queue.empty:
            request = self.queue.get()
            print(f"start inference request {request}")
            link_to_video = request.link_to_video
            path_to_video = self.downloader.download_video(link_to_video)
            result = self.model_inferencer.inference(path_to_video)
            key = self.preview_uploader.upload(result)
            os.remove(path_to_video)
            os.remove(result)
            dict_preview = {"type": self.TYPE, "link_to_video": link_to_video, "s3_key": key} 
            #create_preview_from_dict(dict_preview)
            self.__remove_request(request)
        self.is_started = False


    def __remove_request(self, request: Request):
        db = get_db()

        
    def add_request(self, request: Request):
        self.queue.put(request)
        if not self.is_started:
            self.daemon.start()
            self.is_started = True


def get_Maniqa_Interactor() -> ManiqaInteractor:
    model = ModelProvider().get_maniqa_model()
    frame_extractor = FrameExtractor()
    inferencer = Inferencer(model, frame_extractor) 
    uploader = Uploader()
    downloader = YoutubeDownloader()
    return ManiqaInteractor(inferencer, uploader, downloader)

        


        

