#!/usr/bin/emv python3
"""
解压器工厂模块
"""
import os
import tarfile
from typing import Optional, NoReturn

from decompress.exceptions import (
    CompressedFileNotFoundError,
    CompressedFilePermissionDenyError,
    OutputDirNotFoundError,
    OutputNotDirError,
    OutputDirPermissionDenyError, UnsupportedTypeError,
)
from decompress.tarball_decompressor import TarballDecompressor


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
        # 获取压缩文件的绝对路径，并进行校验
        decompressed_file_path = os.path.realpath(decompressed_file_path)
        self._verify_decompressed_file(decompressed_file_path)
        # 当没有指定解压到某个路径时，默认解压至当前路径
        if output_dir is None:
            output_dir = '.'
        # 获取输出目录的绝对路径，并进行校验
        output_dir = os.path.realpath(output_dir)
        self._verify_output_dir(output_dir)
        # 根据压缩文件的压缩格式，获取对应的解压器类，并进行解压
        decompressor = self._get_decompressor(decompressed_file_path)
        decompressor.decompress(decompressed_file_path, output_dir, max_size, max_count)

    @classmethod
    def _get_decompressor(cls, path: str) -> Optional[TarballDecompressor]:
        """
        解压器工厂方法，根据压缩文件的压缩格式，返回对应的压缩器类
        :param path: 压缩文件路径，可以是相对路径或绝对路径
        :return: 对应的压缩器类
        """
        if tarfile.is_tarfile(path):
            return TarballDecompressor()
        else:
            raise UnsupportedTypeError(path)

    @staticmethod
    def _verify_decompressed_file(path: str) -> NoReturn:
        """
        校验压缩文件
        :param path: 压缩文件路径，可以是相对路径或绝对路径
        :return: None
        """
        path = os.path.realpath(path)
        # 判断压缩文件是否存在
        if not os.path.exists(path):
            raise CompressedFileNotFoundError(path)
        # 判断当前用户对压缩文件是否有读权限
        if not os.access(path, os.R_OK):
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
        # 判断输出目录是否存在
        if not os.path.exists(path):
            raise OutputDirNotFoundError(path)
        # 判断是否是目录
        if not os.path.isdir(path):
            raise OutputNotDirError(path)
        # 判断目录是否有读写执行权限，没有则不能解压到该目录
        if not os.access(path, os.R_OK | os.W_OK | os.X_OK):
            raise OutputDirPermissionDenyError(path)
        # TODO
        # 1. 校验压缩文件解压输出路径是否有足够的空间


if __name__ == '__main__':
    decompressor = Decompressor()
    decompressor.decompress('demo.tar.gz')
