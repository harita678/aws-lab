# ============================================================================
# security-group-rules.tf — Ingress rules - incldue rules for each security group here
# ============================================================================

# Rules(#4) for Web Tier security group

resource "aws_vpc_security_group_ingress_rule" "web_http" {
  security_group_id = aws_security_group.web.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 80
  ip_protocol       = "tcp"
  to_port           = 80
}

resource "aws_vpc_security_group_ingress_rule" "web_ssh" {
  security_group_id = aws_security_group.web.id
  cidr_ipv4         = "76.67.45.97/32"
  from_port         = 22
  ip_protocol       = "tcp"
  to_port           = 22
  description       = "for ssh - allow only from my laptop"
}

resource "aws_vpc_security_group_ingress_rule" "web_app_port" {
  security_group_id = aws_security_group.web.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 8000
  ip_protocol       = "tcp"
  to_port           = 8000
}

resource "aws_vpc_security_group_ingress_rule" "web_dashboard_port" {
  security_group_id = aws_security_group.web.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 8001
  ip_protocol       = "tcp"
  to_port           = 8001
  description       = "Dashboard read API"
}

# --- APP TIER (1 rule) ---
resource "aws_vpc_security_group_ingress_rule" "app_from_web" {
  security_group_id            = aws_security_group.app.id
  from_port                    = 8000
  ip_protocol                  = "tcp"
  to_port                      = 8000
  referenced_security_group_id = aws_security_group.web.id
}

# --- DB TIER (3 rules) ---

resource "aws_vpc_security_group_ingress_rule" "db_from_app" {
  security_group_id            = aws_security_group.db.id
  from_port                    = 5432
  to_port                      = 5432
  ip_protocol                  = "tcp"
  referenced_security_group_id = aws_security_group.app.id
}
#Dashboard (web tier) reads RDS
resource "aws_vpc_security_group_ingress_rule" "db_from_web" {
  security_group_id            = aws_security_group.db.id
  referenced_security_group_id = aws_security_group.web.id
  from_port                    = 5432
  ip_protocol                  = "tcp"
  to_port                      = 5432
}

resource "aws_vpc_security_group_ingress_rule" "db_from_laptop" {
  security_group_id = aws_security_group.db.id
  from_port         = 5432
  to_port           = 5432
  ip_protocol       = "tcp"
  cidr_ipv4         = "76.67.45.97/32"
}