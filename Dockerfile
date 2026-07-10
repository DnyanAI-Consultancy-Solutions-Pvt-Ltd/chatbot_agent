# Use official lightweight Python stable core runtime image
FROM python:3.11-slim

# Set system configurations 
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HF_HOME=/tmp/.cache

WORKDIR /code

# Install system utilities
RUN apt-get update && apt-get install -y git build-essential && rm -rf /lib/apt/lists/*

# Copy configuration registries
COPY ./requirements.txt /code/requirements.txt

# Install python execution layers
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install --no-cache-dir sentence-transformers langchain-groq langchain-huggingface
RUN pip install --no-cache-dir -U chromadb

# Set up non-root user account mapping to comply with Hugging Face policies
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Transfer raw application workspace files into the container
COPY --chown=user . $HOME/app

# Copy the ingestion data script to target /tmp at startup execution
RUN sed -i 's|./database|/tmp/database|g' ingest.py

# Execute data crawling dynamically during initial container boot lifecycle
RUN python ingest.py

# Expose server port bound interface
EXPOSE 7860

# Execute server target daemon runtime engine
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]