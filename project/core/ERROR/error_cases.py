class GlobalErrorMessage(Exception):
    """
        아래와 같은 형태로 사용이 되며,
        단지, message 만 같이 보내기 위해서 사용한다.
        return Response({
            'response': 'error',
            'message': "이게 되지 않습니다."
        })
    """
    pass


class GlobalErrorMessage200(Exception):
    """
        아래와 같은 형태로 사용이 되며,
        단지, message 만 같이 보내기 위해서 사용한다.
        return Response({
            'response': 'error',
            'message': "이게 되지 않습니다."
        })
    """
    pass


class GlobalErrorMessage400(Exception):
    """
        아래와 같은 형태로 사용이 되며,
        단지, message 만 같이 보내기 위해서 사용한다.
        return Response({
            'response': 'error',
            'message': "이게 되지 않습니다."
        })
    """
    pass
