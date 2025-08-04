FROM golang:1.21-alpine AS build
WORKDIR /app
COPY . .
RUN go mod download
RUN go build -o read_products read_products.go

FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=build /app/read_products .
CMD ["./read_products"]
