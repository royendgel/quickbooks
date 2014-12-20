class RequestCreator:
  def create_name(self, object_name, operation, method):
    '''
    Acording to chapter 3 page # 32:
    Naming are sliced in 3 parts object, operation + Rq
    '''
    return "%s%s%s" %(object_name, operation.title(), method.title())