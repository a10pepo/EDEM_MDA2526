terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

data "aws_vpc" "default" {
  count   = local.lookup_default_vpc ? 1 : 0
  default = true
}

data "aws_subnets" "default" {
  count = local.lookup_default_subnets ? 1 : 0

  filter {
    name   = "vpc-id"
    values = [local.rds_vpc_id]
  }
}

locals {
  create_security_group = var.manage_networking && length(var.security_group_ids) == 0
  lookup_default_vpc    = local.create_security_group && var.vpc_id == null
  lookup_default_subnets = (
    var.manage_networking &&
    var.create_db_subnet_group &&
    length(var.subnet_ids) == 0
  )
  rds_vpc_id     = var.manage_networking ? (var.vpc_id != null ? var.vpc_id : data.aws_vpc.default[0].id) : null
  rds_subnet_ids = var.manage_networking ? (length(var.subnet_ids) > 0 ? var.subnet_ids : data.aws_subnets.default[0].ids) : []
  rds_security_group_ids = length(var.security_group_ids) > 0 ? var.security_group_ids : (local.create_security_group ? [
    aws_security_group.rds[0].id
  ] : null)
}

resource "aws_security_group" "rds" {
  count = local.create_security_group ? 1 : 0

  name_prefix = "football-callup-rds-"
  description = "Allow PostgreSQL access for Football Callup Manager"
  vpc_id      = local.rds_vpc_id

  ingress {
    description = "PostgreSQL from allowed CIDR"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [var.allowed_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Project = "football-callup-manager"
  }
}

resource "aws_db_subnet_group" "football" {
  count = var.manage_networking && var.create_db_subnet_group ? 1 : 0

  name       = "${var.db_identifier}-subnet-group"
  subnet_ids = local.rds_subnet_ids

  tags = {
    Project = "football-callup-manager"
  }
}

resource "aws_db_instance" "football" {
  identifier = var.db_identifier

  engine         = "postgres"
  engine_version = var.engine_version
  instance_class = var.db_instance_class

  allocated_storage = var.allocated_storage
  storage_type      = "gp2"

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password
  port     = 5432

  db_subnet_group_name   = var.manage_networking && var.create_db_subnet_group ? aws_db_subnet_group.football[0].name : null
  vpc_security_group_ids = local.rds_security_group_ids
  publicly_accessible    = var.publicly_accessible

  backup_retention_period = 0
  deletion_protection     = false
  skip_final_snapshot     = true

  auto_minor_version_upgrade = true

  tags = {
    Project = "football-callup-manager"
  }
}
