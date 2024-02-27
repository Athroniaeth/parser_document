from dataclasses import dataclass

from src.data.config.node import NodeConfig



class ConfigExtraction(NodeConfig):
    folder_output: str = "06_extracted_bbox_images"
