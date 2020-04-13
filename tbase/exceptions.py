# -*- coding: UTF-8 -*-


class OriException(Exception):
    pass


# normal exception 此类为调用时的预期异常，应当被正确捕获并处理
class OriExpectedException(OriException):
    pass


# Fatal error 此类异常表示无法正常运行当前逻辑，应交由模块外层循环处理并记录日志，通常意味着错误的使用了某些方法或产生了未知错误
class OriFatalError(OriException):
    pass


# PreprocessorException
class PreprocessorException(OriException):
    pass


class ContentTypeInvalid(PreprocessorException, OriExpectedException):
    def __init__(self):
        message = "Http request content-type is not json"
        ContentTypeInvalid.__init__(message)


# MonitorException
class MonitorException(OriException):
    pass

# CommunicatorException
class CommunicatorException(OriException):
    pass



class QueueEmpty(CommunicatorException, OriExpectedException):
    def __init__(self):
        message = "OriQueue which get in communicator is empty"
        super(QueueEmpty, self).__init__(message)


class QueueValueError(CommunicatorException, OriExpectedException):
    def __init__(self):
        message = "OriQueue send data too large"
        super(QueueValueError, self).__init__(message)


class QueueNotExist(CommunicatorException, OriFatalError):
    def __init__(self):
        message = "OriQueue which put in communicator is not exist"
        super(QueueNotExist, self).__init__(message)


class SharedSettingError(CommunicatorException, OriFatalError):
    def __init__(self):
        message = "Try to get Shared Settings before it set"
        super(SharedSettingError, self).__init__(message)

if __name__ == "__main__":
    try:
        raise  QueueValueError()
    except Exception as e:
        print str(e)