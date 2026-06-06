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

# ── Aurora Cluster (Serverless v2) ────────────────────────────────────────────

resource "aws_rds_cluster" "aurora" {
  cluster_identifier     = "almacen-aurora-cluster"
  engine                 = "aurora-postgresql"
  engine_version         = "15.4"
  database_name          = "almacen_db"
  master_username        = var.db_username
  master_password        = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.aurora.name
  vpc_security_group_ids = [aws_security_group.aurora.id]
  skip_final_snapshot    = true
  deletion_protection    = false

  serverlessv2_scaling_configuration {
    min_capacity = 0.5
    max_capacity = 4.0
  }

  tags = {
    Name    = "almacen-aurora-cluster"
    Project = "monitor-expediciones"
  }
}

resource "aws_rds_cluster_instance" "aurora" {
  identifier          = "almacen-aurora-instance"
  cluster_identifier  = aws_rds_cluster.aurora.id
  instance_class      = "db.serverless"
  engine              = aws_rds_cluster.aurora.engine
  engine_version      = aws_rds_cluster.aurora.engine_version
  publicly_accessible = true

  tags = {
    Name    = "almacen-aurora-instance"
    Project = "monitor-expediciones"
  }
}
