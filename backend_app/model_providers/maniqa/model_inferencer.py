# import os

# import numpy as np
# import cv2
# from torchvision import transforms

# from utils.frame_extractor import FrameExtractor
# from model_providers.maniqa.model_provider import ModelProvider
# from utils.model_utils import ToTensor, Normalize

# class Inferencer:

#     CROP_SIZE = 224

#     def __init__(self, model_provider: ModelProvider, frame_extractor: FrameExtractor, output_folder: str = "inference_output"):
#         self.output_folder = output_folder
#         self.model = model_provider.get_maniqa_model()
#         self.frame_extractor = frame_extractor

#     def inference(self, path_to_video: str) -> str:
#         frames = self.frame_extractor.get_frames(path_to_video)
#         max = 0
#         best_frame = None
#         for frame in frames:
#             prepared = self.prepare(frame)
#             img = prepared['d_img_org'].cuda()
#             img = self.random_crop(img)
#             res = self.model(img)
#             if res > max:
#                 max = res
#                 best_frame = frame
#         output_path = self.output_folder + "/" + os.path.basename(path_to_video) + ".jpg"
#         cv2.imwrite(output_path, best_frame)
#         return output_path

#     def __prepare(self, img):
#         d_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         d_img = np.array(d_img).astype('float32') / 255
#         d_img = np.transpose(d_img, (2, 0, 1))
#         sample = {
#             'd_img_org': d_img,
#             'd_name': ""
#         }
#         transform = transforms.Compose([Normalize(0.5, 0.5), ToTensor()])
#         sample = transform(sample)
#         return sample

#     def __random_crop(self, d_img):
#         c, h, w = d_img.shape
#         top = np.random.randint(0, h - self.CROP_SIZE)
#         left = np.random.randint(0, w - self.CROP_SIZE)
#         d_img_org = self.crop_image(top, left, self.CROP_SIZE, img=d_img)
#         d_img_org = d_img_org[None, :]
#         return d_img_org

#     def __crop_image(self, top, left, patch_size, img=None):
#         tmp_img = img[:, top:top + patch_size, left:left + patch_size]
#         return tmp_img


