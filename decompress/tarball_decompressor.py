#!/usr/bin/emv python3
"""
tarball 类型压缩文件解压器模块
"""
import tarfile
from typing import NoReturn

from decompress.base_decompressor import BaseDecompressor
from decompress.exceptions import FileSizeExceedsLimitError, FileCountExceedsLimitError


class TarballDecompressor(BaseDecompressor):

    def decompress(self, path: str, output_dir: str, max_size: int, max_count: int) -> NoReturn:
        """
        解压
        :param path: 压缩文件路径，可以是相对路径或绝对路径
        :param output_dir: 压缩文件输出目录路径，可以是相对路径或绝对路径
        :param max_size: 压缩文件解压后，得到文件大小的上限
        :param max_count: 压缩文件解压后，得到文件数量的上限
        :return: None
        """
        self._verify(path, max_size, max_count)
        with tarfile.open(path) as tf:
            tf.extractall(path=output_dir)

    @staticmethod
    def _verify(path: str, max_size: int, max_count: int) -> NoReturn:
        """
        对压缩文件进行检验，通过设置解压后文件大小上限和文件数量上限，防止压缩炸弹攻击
        :param path: 压缩文件路径，可以是相对路径或绝对路径
        :param max_size: 压缩文件解压后，得到文件大小的上限
        :param max_count: 压缩文件解压后，得到文件数量的上限
        :return: None
        """
        with tarfile.open(path) as tf:
            total_size = 0
            for _ in range(max_count + 1):
                member = tf.next()
                if not member:
                    break
                total_size += member.size
                if total_size > max_size:
                    raise FileSizeExceedsLimitError(path, max_size)
            else:
                raise FileCountExceedsLimitError(path, max_count)
