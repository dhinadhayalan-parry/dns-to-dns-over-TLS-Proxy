# DNS to DNS-over-TLS(DoT) Proxy

## Introduction

Conventional DNS transfer the data over UDP/TCP without encryption leads to vulnerability like spoofing, tampering, and intrusions. One of the mainstream approaches to mitigating such threats is to do encryption of DNS communication. Various techniques have been proposed, including DNS-over-TLS(DoT), DNS-over-HTTPS(DoH), DNSCrypt.
In this project, a proxy for conventional DNS to DNS-over-TLS has been created. So that request from the client listens to the DNS in the port tcp/53, proxy them to the Cloudflare's DoT, and sends the response back to the sender.

## Installation steps

1. Build the docker image from the project root directory and publish the image to the registry.

```bash
$ docker build -t dot-proxy:1.0 .
```

2. Run the container based on the above-built image.

```bash
$ docker run -p 53:53 dot-proxy:1.0
```

3. Test the DNS server query to the localhost nameserver.

```bash
$ dig @localhost -p 53 example.com
```

4. On a successful response, the server will give 200 response code.

## Security Concerns for this kind of Service

DoT proxy is not considered as an End-to-End protocol, only hop-to-hop encrypted. So, there is a possibility for the man in the middle to spoof or hijack the traffic between the client, edit the data packets, and send it over the TCP.

## Microservice Architecture

Microservices architecture is highly recommended as a proxy server as a service on its own distributed servers as a container. So that it is possible to have High availability and easily scalable as per our requirements. The microservice architecture allows this service to be deployed, rebuilt, re-deployed, and managed independently and the issue with one service will not impact or influence the entire system and the failure of individual microservices can be compensated quickly.

## Area of improvements

Multiple aspects can be improvised in this project. Some noted points that are below.

* Multi-threaded can be implemented to process the query in parallel.
* Implementation of caching layer for the high performance.
* Implementation of test cases.
* Redundancy of the upstream DNS server. This will make sure that if one server is down, the query will be sent to another fallback server.
