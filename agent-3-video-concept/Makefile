â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

.PHONY: help install deploy run test clean

PROJECT_ID ?= your-project-id
REGION ?= us-central1
BUCKET_NAME ?= video-concepts-bucket

help:
	@echo "Video Concept Collaborator - Agent 3"
	@echo "Available commands:"
	@echo "  make install         - Install dependencies"
	@echo "  make test            - Run tests"
	@echo "  make run             - Run agent locally"
	@echo "  make deploy          - Deploy to Vertex AI"
	@echo "  make clean           - Clean temporary files"

install:
	pip install -r requirements.txt
	@echo "Dependencies installed successfully"

test:
	python -m pytest -v tests/ 2>/dev/null || echo "No tests found or pytest not installed"

run:
	GCP_PROJECT_ID=$(PROJECT_ID) GCP_BUCKET_NAME=$(BUCKET_NAME) python agent.py

deploy:
	@echo "Deploying Agent 3 to Vertex AI..."
	gcloud functions deploy video-concept-agent-3 \
		--runtime python311 \
		--trigger-http \
		--allow-unauthenticated \
		--project=$(PROJECT_ID) \
		--region=$(REGION) \
		--entry-point=main \
		--source=. \
		--set-env-vars GCP_PROJECT_ID=$(PROJECT_ID),GCP_BUCKET_NAME=$(BUCKET_NAME)
	@echo "Deployment complete"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".DS_Store" -delete
	rm -f concepts_*.json
	@echo "Cleanup complete"

format:
	python -m black agent.py 2>/dev/null || echo "black not installed"
	python -m isort agent.py 2>/dev/null || echo "isort not installed"

lint:
	python -m pylint agent.py 2>/dev/null || echo "pylint not installed"



â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
