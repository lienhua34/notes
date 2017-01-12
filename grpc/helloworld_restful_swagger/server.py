from concurrent import futures
import time

import grpc

import pb.helloworld_pb2 as pb_dot_helloworld__pb2
import pb.helloworld_pb2_grpc as pb_dot_helloworld_pb2__grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class MyServer(pb_dot_helloworld_pb2__grpc.GreeterServicer):
    def SayHello(self, request, context):
        print("Receive request, request.name: {0}".format(request.name))
        return pb_dot_helloworld__pb2.HelloReply(
            message='Hello, {0}'.format(request.name))

    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb_dot_helloworld_pb2__grpc.add_GreeterServicer_to_server(MyServer(), server)
    server.add_insecure_port('[::]:50051')
    print("GreeterServicer start at port 50051...")
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
        
if __name__ == '__main__':
    serve() 
