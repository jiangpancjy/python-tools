#!/usr/bin/emv python3
"""
解压器基类模块
"""
from abc import ABC, abstractmethod
from os import access, R_OK, W_OK, X_OK
from os.path import realpath, exists, isdir
from typing import NoReturn

from decompress.exceptions import CompressedFileNotFoundError, CompressedFilePermissionDenyError, \
    OutputDirNotFoundError, OutputNotDirError, OutputDirPermissionDenyError


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

    @abstractmethod
    def _verify(self, path: str, output_dir: str, max_size: int, max_count: int) -> NoReturn:
        """
        对压缩文件进行检验
        :param path: 压缩文件路径，可以是相对路径或绝对路径
        :param output_dir: 压缩文件输出目录路径，可以是相对路径或绝对路径
        :param max_size: 压缩文件解压后，得到文件大小的上限
        :param max_count: 压缩文件解压后，得到文件数量的上限
        :return: None
        """
        pass

    @staticmethod
    def _verify_decompressed_file(path: str) -> NoReturn:
        """
        校验压缩文件
        :param path: 压缩文件路径，可以是相对路径或绝对路径
        :return: None
        """
        path = realpath(path)
        # 判断压缩文件是否存在
        if not exists(path):
            raise CompressedFileNotFoundError(path)
        # 判断当前用户对压缩文件是否有读权限
        if not access(path, R_OK):
            raise CompressedFilePermissionDenyError(path)
        # TODO
        # 1. 校验压缩文件中是否包含 / 或者 ..

    @staticmethod
    def _verify_output_dir(path: str) -> NoReturn:
        """
        校验输出目录
        :param path: 压缩文件输出目录路径，可以是相对路径或绝对路径
        :return: None
        """
        path = realpath(path)
        # 判断输出目录是否存在
        if not exists(path):
            raise OutputDirNotFoundError(path)
        # 判断是否是目录
        if not isdir(path):
            raise OutputNotDirError(path)
        # 判断目录是否有写执行权限，没有则不能解压到该目录
        if not access(path, W_OK | X_OK):
            raise OutputDirPermissionDenyError(path)
        # TODO
        # 1. 校验压缩文件解压输出路径是否有足够的空间
