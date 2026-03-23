locals {
  my_ip_cidr = "${chomp(data.http.my_ip.response_body)}/32"
}