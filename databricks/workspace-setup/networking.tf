data "aws_availability_zones" "available" {}
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "6.0.1"

  name = "${var.resource_prefix}vpc"
  azs = data.aws_availability_zones.available.names
  cidr = var.aws_vpc_cidr_block

  enable_dns_hostnames = true
  enable_nat_gateway = true
  single_nat_gateway = true
  create_igw = true

  public_subnets = [cidrsubnet(var.aws_vpc_cidr_block, 3, 0)]
  private_subnets = [cidrsubnet(var.aws_vpc_cidr_block, 3, 1), cidrsubnet(var.aws_vpc_cidr_block, 3, 2)]

  manage_default_security_group = true
  default_security_group_name = "db-sg"

  default_security_group_egress = [{
    cidr_blocks = "0.0.0.0/0"
  }]
  default_security_group_ingress = [{
    description = "allow internal TCP and UDP"
    self = true
  }]
}

module "vpc_endpoints" {
  source  = "terraform-aws-modules/vpc/aws//modules/vpc-endpoints"
  version = "3.2.0"
  vpc_id = module.vpc.vpc_id
  security_group_ids = [module.vpc.default_security_group_id]
  endpoints = {
    s3 = {
      service = "s3"
      service_type = "Gateway"
      route_table_ids = flatten([module.vpc.private_route_table_ids, module.vpc.public_route_table_ids])
    },
    sts = {
      service = "sts"
      private_dns_enabled = true
      subnet_ids = module.vpc.private_subnets
    },
    kinesis-streams = {
      service = "kinesis-streams"
    }
  }
}
resource "databricks_mws_networks" "this" {
  provider = databricks.mws
  account_id   = var.db_account_id
  network_name = "${var.resource_prefix}vpc"
  security_group_ids = [module.vpc.default_security_group_id]
  subnet_ids = module.vpc.private_subnets
  vpc_id = module.vpc.vpc_id
}
