import sys
import os
import uuid
import shutil
import datetime
import time
import logging
import base64
import numpy as np
import cv2

import time

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.VideoSave.src.utils.response import build_response
from components.VideoSave.src.models.PackageModel import PackageModel
from sdks.novavision.src.base.application import Application
from sdks.novavision.src.media.image import Image

from components.VideoSave.src.classes.Fps import FPSCounter

logging.basicConfig(level=logging.INFO)


class VideoSave(Component):
    application = Application()

    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))

        self.image = self.request.get_param("inputImage")
        self.input_frames = []  # Boş liste olarak initialize et

        # self.input_frames = self._extract_frames_from_input(self.image)
        self.record_duration = self.request.get_param("recordDuration")
        self.title = self.request.get_param("videoTitle") or "untitled_video"
        self.user_fps = self.request.get_param("configFps")
        self.system_control = self.request.get_param("systemControl")

        raw_target = self.request.get_param("configTargetDirectory")
        if isinstance(raw_target, dict):
            self.target_type = raw_target.get("value", {}).get("value", "TargetLocal")
        else:
            self.target_type = raw_target or "TargetLocal"

        self.local_path = "/storage/videos"
        os.makedirs(self.local_path, exist_ok=True)

        self.temp_dir = "/storage/temp"
        self.logger = logging.getLogger(__name__)

        self.fps_counter = FPSCounter(update_interval=4.0)


    @staticmethod
    def bootstrap(config: dict):
        video_name = VideoSave.application.get_param(config=config, name="videoTitle")
        return {"video_name": video_name, "outputVideoUrl": None}




    def run(self):
        """Her frame geldiğinde otomatik çalışan metod"""
        self.image = Image.get_frame(img=self.image, redis_db=self.redis_db)

        print("Frame geldi", time.time())

        # FPS güncelle
        self.fps_counter.update()
        print("FPS Counter frame count:", self.fps_counter.frame_count)
        print("Anlık FPS:", self.fps_counter.get_fps())

        current_fps = self.fps_counter.get_fps()
        if current_fps > 0:
            print(f"FPS: {current_fps:.2f}")

        print(f"FPS: {current_fps:.2f}")


        packageModel = build_response(context=self)
        return packageModel


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
