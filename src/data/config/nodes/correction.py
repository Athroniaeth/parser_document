from dataclasses import dataclass

from src.data.config.node import NodeConfig



class ConfigCorrection(NodeConfig):
    folder_output: str = "05_corrected_images"
