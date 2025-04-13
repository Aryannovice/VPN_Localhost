run openssl req -x509 -newkey rsa:4096 -keyout vpn_server/ssl/server.key -out vpn_server/ssl/server.crt -days 365 -nodes in the bash first
While inputting ssl values , ensure FQDN is same as IP of client
copy vpn_server\ssl\server.crt vpn_client\ssl\ //in bash
ensure your exports are proper , to export aes_hardcoded / aes_h2 , make changes in this line  from vpn_server.utils import encrypt_data, decrypt_data  
the order of execution is proxy - server - client

/n

All the best
