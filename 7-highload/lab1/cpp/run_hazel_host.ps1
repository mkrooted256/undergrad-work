param([string]$ip, [int]$port=5701)

echo "port: $port"
echo "ip: $ip"
docker run -d --network hazel --ip "172.18.0.${ip}" -e "HZ_NETWORK_PUBLICADDRESS=172.18.0.${ip}:${port}" hazelcast/hazelcast:4.2.6
