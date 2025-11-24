# ============================================
# FROM AIR TO CARE - DOCKER CONFIGURATION
# ============================================

# Step 1: Use Python 3.11 as base image
FROM python:3.11-slim

# Step 2: Set working directory inside container
WORKDIR /app

# Step 3: Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Step 4: Copy requirements first (for caching)
COPY requirements.txt .

# Step 5: Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Copy all project files
COPY . .

# Step 7: Create directories for outputs
RUN mkdir -p models artifacts mlruns data/raw

# Step 8: Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Step 9: Expose port for API
EXPOSE 8000

# Step 10: Use entrypoint script
ENTRYPOINT ["python", "entrypoint.py"]

# Step 11: Default command (train)
# CMD ["train"]
# 确保最后一行是：
# Step 11: Default command (serve for API)
CMD ["serve"]
