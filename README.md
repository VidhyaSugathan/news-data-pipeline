News Sentiment Data Pipeline

A serverless, event-driven data pipeline that ingests live news articles every 5 minutes, scores their sentiment, and displays the results on a real-time analytics dashboard — built entirely on AWS.

Architecture
EventBridge (5-min schedule)
        │
        ▼
   AWS Lambda ──► NewsAPI (fetch articles)
        │
        ├──► VADER sentiment analysis
        ├──► Raw JSON → Amazon S3 (backup/audit trail)
        └──► Structured rows → Amazon RDS (PostgreSQL)
                          │
                          ▼
                 Amazon ECS Fargate
                 (Dockerized Streamlit dashboard)
                          │
                          ▼
                  Live public dashboard

Flow: EventBridge triggers a Lambda function every 5 minutes. The function fetches the latest headlines from NewsAPI, scores each article's sentiment, archives the raw response in S3, and writes clean structured records to a PostgreSQL database on RDS. A separate, containerized Streamlit dashboard — deployed on ECS Fargate — reads from that same database and displays live sentiment trends.

Tech Stack
Layer	Technology
Ingestion / compute	AWS Lambda (Python)
Scheduling	Amazon EventBridge
Raw data storage	Amazon S3
Database	Amazon RDS (PostgreSQL)
Sentiment analysis	VADER (vaderSentiment)
Dashboard	Streamlit
Containerization	Docker
Container registry	Amazon ECR
Container hosting	Amazon ECS (Fargate)
Project Structure
news-data-pipeline/
├── lambda/                 # Ingestion function (deployed to AWS Lambda)
│   ├── app.py               # Entry point (lambda_handler)
│   ├── news_api.py          # Fetches articles from NewsAPI
│   ├── sentiment.py         # Scores sentiment using VADER
│   ├── s3_upload.py         # Archives raw JSON to S3
│   ├── db.py                # PostgreSQL connection (psycopg2)
│   ├── config.py            # API key configuration
│   └── requirements.txt
│
├── dashboard/               # Streamlit dashboard (deployed to ECS Fargate)
│   ├── app.py                # Reads from RDS, renders charts
│   ├── Dockerfile
│   └── requirements.txt
│
├── sql/
│   └── create_table.sql      # Database schema
│
└── README.md
Dashboard Features
KPI summary: total articles, most common sentiment, distinct sources
Sentiment breakdown (positive / negative / neutral)
Sentiment trend over time
Sentiment comparison across news sources
Live table of the latest articles
Running Locally

Dashboard:

bash
cd dashboard
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py

Requires a .env file in dashboard/ with:

DB_HOST=<your-postgres-host>
DB_PORT=5432
DB_NAME=<your-db-name>
DB_USER=<your-db-user>
DB_PASSWORD=<your-db-password>

Lambda function (tested locally as a plain script before packaging for deployment):

bash
cd lambda
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py

Requires a .env file in lambda/ with the same database variables above, plus:

NEWS_API_KEY=<your-newsapi-key>
AWS_REGION=<your-region>
S3_BUCKET_NAME=<your-bucket-name>
Deployment Notes
The Lambda function is packaged with Linux-compatible dependencies (pip install --platform manylinux2014_x86_64 --only-binary=:all:) since AWS Lambda runs on Linux regardless of the development machine's OS.
The dashboard is built as a Docker image, pushed to Amazon ECR, and run as an ECS Fargate service for continuous availability.
Database credentials are injected via environment variables at the Lambda/ECS level — no secrets are stored in the repository (.env files are git-ignored).
Engineering Challenges Solved
Cross-platform dependency mismatch: psycopg2 compiled for Windows failed on Lambda's Linux runtime — resolved by explicitly targeting the Linux platform during packaging.
Read-only Lambda filesystem: local file writes failed in Lambda since only /tmp is writable there — redirected accordingly.
Network debugging: used AWS Reachability Analyzer to systematically verify security groups, network ACLs, and routing when the dashboard was initially unreachable, isolating the issue to a local network/ISP port restriction rather than an AWS misconfiguration.
License

Personal portfolio project — built for learning and demonstration purposes.
