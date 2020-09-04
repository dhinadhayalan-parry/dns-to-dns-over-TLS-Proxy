import socket
import ssl
import sys
import thread
import binascii

# Convert the UDP DNS query to TCP DNS query.
def convertquery(dns_query):
  length = "\x00"+chr(len(dns_query))
  _query = length + dns_query
  return _query

# Sending TCP DNS Query to the Cloudflare DNS server.
def sendquery(tls_conn_sock,dns_query):
  tcp_query=convertquery(dns_query)
  tls_conn_sock.send(tcp_query)
  result=tls_conn_sock.recv(1024)
  return result


# TLS Connection with the Cloudflare server
def tcpconnection(DNS):
  # Create socket
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.settimeout(100)

  # Wrap Socket
  context = ssl.create_default_context()
  context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
  context.verify_mode = ssl.CERT_REQUIRED
  context.load_verify_locations('/etc/ssl/certs/ca-certificates.crt')
  wrappedSocket = context.wrap_socket(sock, server_hostname=DNS)

  # CONNECT AND PRINT REPLY
  wrappedSocket.connect((DNS , 853))
  print(wrappedSocket.getpeercert())

  # Close socket connection
  return wrappedSocket

#------ handle requests
def handler(data,address,DNS):
  tls_conn_sock=tcpconnection(DNS)
  tcp_result = sendquery(tls_conn_sock, data)
  if tcp_result:
     rcode = tcp_result[:6].encode("hex")
     rcode = str(rcode)[11:]
     if (int(rcode, 16) ==1):
        print ("not a dns query")
     else:
	udp_result = tcp_result[2:]
        s.sendto(udp_result,address)
        print ("200")
  else:
     print ("not a dns query")

if __name__ == '__main__':
   DNS = '1.1.1.1'
   port = 53
   host='localhost'
   try:
      s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      s.bind((host, port))
      while True:
        data,address = s.recvfrom(1024)
        thread.start_new_thread(handler,(data, address, DNS))
   except Exception, e:
      print (e)
      s.close()
