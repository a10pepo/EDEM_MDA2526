terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

# ── Networking ────────────────────────────────────────────────────────────────

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

resource "aws_security_group" "rds" {
  name        = "aerodrome-rds-sg"
  description = "Allow PostgreSQL inbound for Aerodrome RDS"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "PostgreSQL"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_subnet_group" "aerodrome" {
  name       = "aerodrome-subnet-group"
  subnet_ids = data.aws_subnets.default.ids
}

# ── RDS PostgreSQL ────────────────────────────────────────────────────────────

resource "aws_db_instance" "aerodrome" {
  identifier        = "aerodrome-db"
  engine            = "postgres"
  engine_version    = "16.3"
  instance_class    = "db.t3.micro"
  allocated_storage = 20
  storage_type      = "gp2"

  db_name  = "aerodrome"
  username = "aerodrome"
  password = var.db_password

  db_subnet_group_name   = aws_db_subnet_group.aerodrome.name
  vpc_security_group_ids = [aws_security_group.rds.id]

  publicly_accessible     = true
  skip_final_snapshot     = true   # allows clean terraform destroy
  backup_retention_period = 0

  tags = {
    Project     = "aerodrome"
    Environment = "dev"
  }
}
