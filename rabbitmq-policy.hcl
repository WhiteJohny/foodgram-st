path "rabbitmq/creds/rabbit" {
  capabilities = ["read"]
}

path "sys/leases/renew" {
  capabilities = ["update"]
}
