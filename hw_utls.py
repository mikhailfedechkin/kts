from PIL import Image

import requests
import re
import json
import time
import logging
from datetime import datetime
import random
import math
import sys
import inspect

#for mypy
from typing import Any
from typing import List

import logging

# global vars
chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
chars_list = list(chars)
interval = len(chars) / 256

### logging configuration 
logging.basicConfig
hw_logger = logging.getLogger("hw_logging")
file_handler = logging.FileHandler("hw.log")

hw_logs_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(hw_logs_formatter)
hw_logger.addHandler(file_handler)

logging.getLogger("urllib3").setLevel(logging.CRITICAL)
logging.getLogger("PIL").setLevel(logging.CRITICAL)
###


def time_measure_decorator(decorated_function):
    def warapper(*args, **kwrg):
        current_stack_index = len(inspect.stack(0)) - 3
        begin_exec = datetime.now()
        indent = ""
        for _ in range(current_stack_index):
            indent += "\t"

        hw_logger.warning(
            f"{indent}>>>> START: {decorated_function.__name__} \
        AT: {begin_exec}"
        )
        decorated_function_result = decorated_function(*args, **kwrg)
        end_exec = datetime.now()
        hw_logger.warning(
            f"{indent}<<<< END: {decorated_function.__name__}  \
        AT: {end_exec} TTL_EXEC_TIME: {end_exec-begin_exec}"
        )

        return decorated_function_result

    return warapper


def get_file_name_from_url(arg_url: str):
    file_name = arg_url.split("/")[-1]
    file_name = file_name.split("?")[0]

    return file_name


class ddg_image:
    url = "https://duckduckgo.com/"

    headers = {
        "authority": "duckduckgo.com",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "sec-fetch-dest": "empty",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4)"
        "AppleWebKit/537.36 (KHTML, like Gecko)"
        "Chrome/80.0.3987.163 Safari/537.36",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "referer": "https://duckduckgo.com/",
        "accept-language": "en-US,en;q=0.9",
    }

    def __init__(self, keyword: str):
        self.search_result: List[str] = []
        self.search(keyword)
        self.picture_index = -1

    def set_picture_index(self, picture_index: int = 0):
        self.picture_index = picture_index

    def set_random_picture_index(self):
        self.picture_index = random.randint(0, len(self.search_result))

    def get_random_image(self):
        self.set_random_picture_index()
        return self.get_picture()

    def get_picture_by_index(self, picture_index: int):
        self.set_picture_index(picture_index)
        return self.get_picture()

    def save_random_image_to_file(self):
        self.set_random_picture_index()
        self.save_image_to_file()

    def save_image_to_file_by_index(self, picture_index: int = 0):
        self.set_picture_index(picture_index)
        self.save_image_to_file()

    @time_measure_decorator
    def save_image_to_file(self) -> str:
        picture_object = self.get_picture()

        try:
            with open(picture_object["filename"], "wb") as picture_file:
                picture_file.write(picture_object["content"])

            return picture_object["filename"]

        except BaseException:
            return ""

    @time_measure_decorator
    def get_picture(self) -> dict:
        return {
            "filename": get_file_name_from_url(self.search_result[self.picture_index]),
            "content": requests.get(self.search_result[self.picture_index]).content,
        }

    @time_measure_decorator
    def picture_to_ascii(self, scale: float = 0.4):
        def pixel_to_char(pixel: int):
            return chars_list[math.floor(pixel * interval)]

        self.get_picture()
        picture_file_name = self.save_image_to_file()
        img_dsr = Image.open(picture_file_name)
        width, height = img_dsr.size
        img_dsr = img_dsr.resize(
            (int(width * scale), int(height * scale)), Image.NEAREST
        )

        width, height = img_dsr.size
        img_obj = img_dsr.load()

        text_file_with_picture = open(f"{picture_file_name}.txt", "w")

        for i in range(height):
            for j in range(width):
                r, g, b = img_obj[j, i]
                pixel = int(r / 3 + g / 3 + b / 3)
                img_obj[j, i] = (pixel, pixel, pixel)
                text_file_with_picture.write(pixel_to_char(pixel))
            text_file_with_picture.write("\n")

    @time_measure_decorator
    def search(self, keywords: str, max_results=None) -> list:

        requestUrl = ddg_image.url + "i.js"
        res = requests.post(ddg_image.url, data={"q": keywords})
        searchObj = re.search(r"vqd=([\d-]+)\&", res.text, re.M | re.I)

        if not searchObj:
            hw_logger.crtical("Token Parsing Failed !")
            return []

        params = (
            ("l", "us-en"),
            ("o", "json"),
            ("q", keywords),
            ("vqd", searchObj.group(1)),
            ("f", ",,,"),
            ("p", "1"),
            ("v7exp", "a"),
        )

        while True:
            while True:
                try:
                    res = requests.get(
                        requestUrl, headers=ddg_image.headers, params=params
                    )
                    data: Any = json.loads(res.text)

                    for item in data["results"]:
                        self.search_result.append(item["image"])
                    break

                except ValueError as e:
                    hw_logger.exception(e)
                    hw_logger.warning("Hitting Url Failure - Sleep and Retry: %s", requestUrl)
                    time.sleep(5)
                    continue

            if not hasattr(data, "next"):
                return self.search_result

            requestUrl = ddg_image.url + data["next"]
        return []


if __name__ == "__main__":

    args = sys.argv
    for arg in args:
        if arg.find("--keyword") != -1:
            comandline_keyword = arg.split("=")[1]
            ddg_images_obj = ddg_image(comandline_keyword)
            ddg_images_obj.set_random_picture_index()
            ddg_images_obj.picture_to_ascii()
