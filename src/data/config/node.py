from pydantic import BaseModel


class NodeConfig(BaseModel):
    folder_output: str
