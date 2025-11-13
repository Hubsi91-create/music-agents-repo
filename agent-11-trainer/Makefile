.PHONY: install test deploy logs clean

install:
pip install -r requirements.txt

test:
python -m pytest tests/ -v

deploy:
gcloud functions deploy agent_11_orchestrator \
--runtime python311 \
--trigger-http \
--entry-point main \
--project=\ \
--region=\

logs:
gcloud functions logs read agent_11_orchestrator --limit 50

clean:
rm -rf __pycache__ *.pyc .pytest_cache
