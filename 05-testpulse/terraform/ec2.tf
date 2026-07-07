# ============================================================================
# EC2.tf — EC2 for TestPulse
# ============================================================================


resource "aws_instance" "ingestor" {
  # Core Configuration
  ami                  = "ami-0d19d7a9bc91b3550"
  instance_type        = "t3.micro"
  key_name             = "my-first-ec2-key"
  iam_instance_profile = aws_iam_instance_profile.ec2.name

  # Network Association
  subnet_id              = "subnet-062db854eb6c2a5bd"
  vpc_security_group_ids = [aws_security_group.web.id]

  #User Data - it is available on EC2 instance
  user_data = file("${path.module}/user-data-ingestor.sh")

  tags = {
    Name        = "harita-testpulse-ingestor"
    Environment = var.environment
    ManagedBy   = "Terraform"
    Project     = "TestPulse"
  }

}