#!/usr/bin/emv python3
"""
解压器工厂模块
"""
from os.path import dirname, realpath
from tarfile import is_tarfile
from typing import Optional, NoReturn, Union
from zipfile import is_zipfile

from decompress.exceptions import (
    UnsupportedTypeError,
)
from decompress.tarball_decompressor import TarballDecompressor
from decompress.zip_decompressor import ZipDecompressor


class Decompressor:

    def decompress(
            self,
            decompressed_file_path: str,
            output_dir: Optional[str] = None,
            max_size: int = 1 * 1024 * 1024 * 1024,
            max_count: int = 10000,
    ) -> NoReturn:
        """
        对压缩文件进行解压，可指定压缩文件的解压路径，以及压缩文件解压后文件大小上限和文件数量上限
        :param decompressed_file_path: 压缩文件路径，可以是相对路径或绝对路径
        :param output_dir: 压缩文件输出目录路径，可以是相对路径或绝对路径
        :param max_size: 压缩文件解压后，得到文件大小的上限
        :param max_count: 压缩文件解压后，得到文件数量的上限
        :return: None
        """
        # 当没有指定解压到某个路径时，默认解压至当前路径
        if output_dir is None:
            output_dir = dirname(realpath(decompressed_file_path))
        # 根据压缩文件的压缩格式，获取对应的解压器类，并进行解压
        decompressor = self._get_decompressor(decompressed_file_path)
        decompressor.decompress(decompressed_file_path, output_dir, max_size, max_count)

    @classmethod
    def _get_decompressor(cls, path: str) -> Union[TarballDecompressor, ZipDecompressor]:
        """
        解压器工厂方法，根据压缩文件的压缩格式，返回对应的压缩器类
        :param path: 压缩文件路径，可以是相对路径或绝对路径
        :return: 对应的压缩器类
        """
        if is_tarfile(path):
            return TarballDecompressor()
        elif is_zipfile(path):
            return ZipDecompressor()
        else:
            raise UnsupportedTypeError(path)
