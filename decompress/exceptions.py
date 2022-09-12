#!/usr/bin/emv python3
"""
解压功能包自定义异常类模块
"""
from typing import Tuple


class CompressedFileNotFoundError(Exception):
    """
    当压缩文件路径不存在时，抛出该异常
    """

    def __init__(self, path: str):
        self.path = path

    def __str__(self):
        return f'compressed file {self.path} not found'


class CompressedFilePermissionDenyError(Exception):
    """
    当压缩文件没有相应权限时，抛出该异常
    """

    def __init__(self, path: str):
        self.path = path
        
    def __str__(self):
        return f'cannot decompress {self.path}, permission denied'


class OutputDirNotFoundError(Exception):
    """
    当压缩文件输出目录路径不存在时，抛出该异常
    """

    def __init__(self, path: str):
        self.path = path

    def __str__(self):
        return f'output directory {self.path} not found'


class OutputNotDirError(Exception):
    """
    当压缩文件输出目录实际上不是一个目录时，抛出该异常
    """

    def __init__(self, path: str):
        self.path = path

    def __str__(self):
        return f'{self.path} not a directory'


class OutputDirPermissionDenyError(Exception):
    """
    当压缩文件输出目录没有对应权限时，抛出该异常
    """

    def __init__(self, path: str):
        self.path = path

    def __str__(self):
        return f'cannot decompress file to {self.path}, permission denied'


class FileSizeExceedsLimitError(Exception):
    """
    当压缩文件解压后，生成的文件总大小超过指定上限时，抛出该异常
    """
    UNITS = ('B', 'KB', 'MB', 'GB', 'TB', 'PB')

    def __init__(self, path: str, max_size: int):
        self.path = path
        tuple_ = self._convert_size(max_size)
        self.max_size = tuple_[0]
        self.unit = tuple_[1]

    def __str__(self):
        return f'after {self.path} is decompressed, the file size exceeds {self.max_size} {self.unit}'

    @staticmethod
    def _convert_size(max_size: int) -> Tuple[int, str]:
        """
        将文件大小转换为人类可读的形式
        :param max_size: 文件大小上限，单位为 Bit
        :return: 返回转换后的文件大小上限、单位
        """
        for unit in FileSizeExceedsLimitError.UNITS:
            if max_size > 1024:
                max_size = max_size / 1024
                continue
            return max_size, unit
        else:
            return max_size, unit


class FileCountExceedsLimitError(Exception):
    """
    当压缩文件解压后，生成的文件数量超过指定上限时，抛出该异常
    """

    def __init__(self, path: str, max_count: int):
        self.path = path
        self.max_count = max_count

    def __str__(self):
        return f'after {self.path} is decompressed, the file count exceeds {self.max_count}'


class UnsupportedTypeError(Exception):
    """
    当解压的压缩文件类型不被支持时，抛出该异常
    """

    def __int__(self, path):
        self.path = path

    def __str__(self):
        return f'the compression format used by {self.path} is not supported'
