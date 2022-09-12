#!/usr/bin/emv python3
"""
解压器基类模块
"""
from abc import ABC, abstractmethod
from typing import NoReturn


class BaseDecompressor(ABC):

    @abstractmethod
    def decompress(self, path: str, output_dir: str, max_size: int, max_count: int) -> NoReturn:
        """
        解压
        :param path: 压缩文件路径，可以是相对路径或绝对路径
        :param output_dir: 压缩文件输出目录路径，可以是相对路径或绝对路径
        :param max_size: 压缩文件解压后，得到文件大小的上限
        :param max_count: 压缩文件解压后，得到文件数量的上限
        :return: None
        """
        pass

    @staticmethod
    @abstractmethod
    def _verify(path: str, max_size: int, max_count: int) -> NoReturn:
        """
        对压缩文件进行检验，通过设置解压后允许的文件大小上限和文件数量上限，防止压缩炸弹攻击
        :param path: 压缩文件路径，可以是相对路径或绝对路径
        :param max_size: 压缩文件解压后，得到文件大小的上限
        :param max_count: 压缩文件解压后，得到文件数量的上限
        :return: None
        """
        pass

