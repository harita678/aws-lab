# ============================================================================
# default-vpc-data.tf — I am using default vpc so I dont need to create the separate resource here; in this file we are just referencing it.
# ============================================================================

data "aws_vpc" "default" {
  id = "vpc-0195a8984f6090bc2"
}