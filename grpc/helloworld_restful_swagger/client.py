import grpc
import pb.helloworld_pb2 as pb_dot_helloworld__pb2
import pb.helloworld_pb2_grpc as pb_dot_helloworld_pb2__grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = pb_dot_helloworld_pb2__grpc.GreeterStub(channel)
    response = stub.SayHello(pb_dot_helloworld__pb2.HelloRequest(name="world"))
    print("GreeterService client received: " + response.message)
    
if __name__ == '__main__':
    run() 
