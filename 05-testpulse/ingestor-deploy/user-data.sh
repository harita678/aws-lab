#!/bin/bash
#
# TestPulse Ingestor — EC2 User Data Bootstrap Script
# Runs ONCE on first boot of an Amazon Linux 2023 EC2 instance
#

# ---------------------------------------------------------------------------
# Section 1: Logging — capture everything for debugging
# ---------------------------------------------------------------------------
exec > /var/log/user-data.log 2>&1
set -x

echo "===== TestPulse Ingestor bootstrap starting at $(date) ====="

# ---------------------------------------------------------------------------
# Section 2: System update
# ---------------------------------------------------------------------------
echo "Updating system packages..."
dnf update -y

# ---------------------------------------------------------------------------
# Section 3: Install Python 3.12
# ---------------------------------------------------------------------------
echo "Installing Python 3.12..."
dnf install -y python3.12 python3.12-pip

# ---------------------------------------------------------------------------
# Section 4: Install git
# ---------------------------------------------------------------------------
echo "Installing git..."
dnf install -y git

# ---------------------------------------------------------------------------
# Section 5: Clone the repo (as ec2-user, not root)
# ---------------------------------------------------------------------------
echo "Cloning aws-lab repo..."
cd /home/ec2-user
sudo -u ec2-user git clone -b feat/testpulse-lambda-processor https://github.com/harita678/aws-lab.git

# ---------------------------------------------------------------------------
# Section 6: Install Python dependencies
# ---------------------------------------------------------------------------
echo "Installing Python dependencies..."
cd /home/ec2-user/aws-lab/05-testpulse/ingestor
sudo -u ec2-user pip3.12 install --user -r requirements.txt

# ---------------------------------------------------------------------------
# Section 7: Write .env file with config
# ---------------------------------------------------------------------------
echo "Writing .env file..."
cat > /home/ec2-user/aws-lab/05-testpulse/ingestor/.env << 'EOF'
AWS_REGION=ca-central-1
S3_BUCKET=harita-testpulse-raw-2026
SQS_QUEUE_URL=https://sqs.ca-central-1.amazonaws.com/951125265513/harita-testpulse-ingestion-queue
EOF
chown ec2-user:ec2-user /home/ec2-user/aws-lab/05-testpulse/ingestor/.env

# ---------------------------------------------------------------------------
# Section 8: Create systemd service file
# ---------------------------------------------------------------------------
echo "Creating systemd service..."
cat > /etc/systemd/system/testpulse-ingestor.service << 'EOF'
[Unit]
Description=TestPulse Ingestor (FastAPI)
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/aws-lab/05-testpulse/ingestor
EnvironmentFile=/home/ec2-user/aws-lab/05-testpulse/ingestor/.env
ExecStart=/home/ec2-user/.local/bin/uvicorn app:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# ---------------------------------------------------------------------------
# Section 9: Enable + start the service
# ---------------------------------------------------------------------------
echo "Enabling and starting Ingestor service..."
systemctl daemon-reload
systemctl enable testpulse-ingestor
systemctl start testpulse-ingestor

# ---------------------------------------------------------------------------
# Section 10: Done
# ---------------------------------------------------------------------------
echo "===== TestPulse Ingestor bootstrap completed at $(date) ====="
echo "Check status: systemctl status testpulse-ingestor"
echo "Check logs:   journalctl -u testpulse-ingestor -f"