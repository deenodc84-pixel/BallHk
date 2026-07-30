FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY bot.py config.py mood_data.json ./

# Run the bot
CMD ["python", "bot.py"]
