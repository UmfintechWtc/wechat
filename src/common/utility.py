import os
import random
from typing import Any, Union, List


class Dict2Obj(object):
    """
    Returns: dict -> obj
    """

    def __init__(self, map_):
        self.map_ = map_

    def __getattr__(self, name) -> Union['Dict2Obj', List[Any], Any]:
        val = self.map_.get(name)
        if isinstance(val, dict):
            return Dict2Obj(val)
        elif isinstance(val, list):
            return [item for item in val]
        else:
            return self.map_.get(name)

    def __str__(self) -> str:
        return str(self.map_)

    def __getitem__(self, key: Any) -> Any:
        return self.map_[key]


def CreateDirectory(targetPath: str):
    """_summary_
    Args:
        targetPath (str): 创建目录
    """
    if not os.path.exists(targetPath):
        os.makedirs(targetPath)


def RandomStr():
    """ 随机生成16位字符串
    @return: 16位字符串
    """
    return str(random.randint(1000000000000000, 9999999999999999)).encode()
