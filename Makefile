start:
	@echo "Start API server"
	rm -r ~/.cache/torch_extensions/*
	python -m uvicorn main:app
