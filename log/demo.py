from logging import getLogger, StreamHandler, Formatter, DEBUG


def init_log(log_file_path):
    # 创建记录器
    logger = getLogger(log_file_path)
    logger.setLevel(DEBUG)

    # 创建控制台处理器
    stream_handler = StreamHandler()
    stream_handler.setLevel(DEBUG)

    # 创建格式化器
    formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 控制器增加格式化器
    stream_handler.setFormatter(formatter)

    # 记录器增加处理器
    logger.addHandler(stream_handler)

    return logger
