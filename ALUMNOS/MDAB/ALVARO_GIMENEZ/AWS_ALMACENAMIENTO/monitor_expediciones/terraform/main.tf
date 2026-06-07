terraform {
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

# ── Security Group ────────────────────────────────────────────────────────────

resource "aws_security_group" "aurora" {
  name        = "almacen-aurora-sg"
  description = "Permite acceso PostgreSQL desde la IP local"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "PostgreSQL desde IP local"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["${var.my_ip}/32"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name    = "almacen-aurora-sg"
    Project = "monitor-expediciones"
  }
}

# ── Subnet Group ─────────────────────────────────────────────────────────────

resource "aws_db_subnet_group" "aurora" {
  name       = "almacen-aurora-subnet-group"
  subnet_ids = data.aws_subnets.default.ids

  tags = {
    Name    = "almacen-aurora-subnet-group"
    Project = "monitor-expediciones"
  }
}

# ── RDS PostgreSQL (Free Tier: db.t3.micro) ───────────────────────────────────

resource "aws_db_instance" "postgres" {
  identifier        = "almacen-postgres"
  engine            = "postgres"
  engine_version    = "15"
  instance_class    = "db.t3.micro"
  allocated_storage = 20
  storage_type      = "gp2"

  db_name  = "almacen_db"
  username = var.db_username
  password = var.db_password

  db_subnet_group_name   = aws_db_subnet_group.aurora.name
  vpc_security_group_ids = [aws_security_group.aurora.id]
  publicly_accessible    = true
  skip_final_snapshot    = true
  deletion_protection    = false

  tags = {
    Name    = "almacen-postgres"
    Project = "monitor-expediciones"
  }
}
