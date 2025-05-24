# Sử dụng image Python slim để giảm kích thước
FROM python:3.9-slim

# Đặt thư mục làm việc
WORKDIR /app

# cài đặt dependencies
RUN pip install --no-cache-dir Flask==2.3.3 openai==1.75.0 werkzeug==3.0.1 pillow

# Mở cổng 5000 cho Flask
EXPOSE 5000

# # Lệnh chạy ứng dụng Flask
# CMD ["python", "app.py"]