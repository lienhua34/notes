package main

import (
	"flag"
	"log"
	"net/http"

	"github.com/grpc-ecosystem/grpc-gateway/runtime"
	"golang.org/x/net/context"
	"google.golang.org/grpc"

	gw "github.com/lienhua34/notes/grpc/helloworld_restful_swagger/pb"
)

var (
	greeterEndpoint = flag.String("helloworld_endpoint", "localhost:50051", "endpoint of Greeter gRPC Service")
)

func run() error {
	ctx := context.Background()
	ctx, cancel := context.WithCancel(ctx)
	defer cancel()

	mux := runtime.NewServeMux()
	opts := []grpc.DialOption{grpc.WithInsecure()}
	err := gw.RegisterGreeterHandlerFromEndpoint(ctx, mux, *greeterEndpoint, opts)
	if err != nil {
		return err
	}

	log.Print("Greeter gRPC Server gateway start at port 8080...")
	http.ListenAndServe(":8080", mux)
	return nil
}

func main() {
	flag.Parse()

	if err := run(); err != nil {
		log.Fatal(err)
	}
}
