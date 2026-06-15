FROM python:3.12-slim
# set work directory
WORKDIR /app
# copy requirements file first
COPY requirements.txt .
# install dependencies
RUN pip install --no-cache-dir -r requirements.txt
# copy project files
COPY . .
# expose port
EXPOSE 8000
# run the app; cmd command
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
