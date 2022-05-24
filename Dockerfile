FROM golang:1.18.2-alpine AS builder
WORKDIR /build
COPY go.mod go.sum *.go ./
run CGO_ENABLED=0 GOOS=linux go build -installsuffix cgo



FROM alpine:3.16.0
WORKDIR /app
COPY --from=builder /build/devops_test ./
CMD ["./devops_test"]
