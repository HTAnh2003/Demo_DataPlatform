# Demo\_DataPlatform

## Mô tả

Dự án triển khai và phục vụ mô hình `TienAnh/Finetune_OCR_1B` sử dụng `vllm`.

---

## Yêu cầu

* **Python**: 3.8+
* **GPU**: Hỗ trợ CUDA
* **Thư viện cần thiết**: `vllm`, `torch`

---

## Hướng dẫn sử dụng

### 1. Chạy server

```bash
vllm serve TienAnh/Finetune_OCR_1B --port 8000 --dtype=auto --tensor-parallel-size 2
```

* `--port`: Cổng server (mặc định 8000).
* `--dtype=auto`: Tự động chọn loại dữ liệu.
* `--tensor-parallel-size=2`: Chạy song song trên 2 GPU.

### 2. Truy cập server

```plaintext
http://localhost:8000
```

> Nếu chạy trên máy chủ từ xa, thay `localhost` bằng địa chỉ IP của máy chủ.

---

## API Mẫu

API mẫu được tham khảo trong file `app.py`. File này bao gồm các chức năng:

1. **Upload hình ảnh**: Tải lên ảnh và gửi tới server OCR.
2. **Hiển thị kết quả**: Trả về văn bản OCR từ hình ảnh đã xử lý.

---

## Cách chạy giao diện web

### 1. Sử dụng Flask App

Chạy file `app.py`:

```bash
python app.py
```

Truy cập giao diện web tại:

```plaintext
http://localhost:5000
```

### 2. Sử dụng Docker Compose

Sử dụng file `docker-compose.yml` để khởi chạy ứng dụng với domain riêng:

```bash
docker-compose up
```

Truy cập ứng dụng theo domain được cấu hình.

---
## Lưu ý
* Đảm bảo đã cài đặt đầy đủ các thư viện cần thiết.
* Kiểm tra kết nối mạng nếu gặp lỗi khi truy cập server.
* Nếu gặp lỗi về GPU, kiểm tra driver và cài đặt CUDA.
* Để dừng server, sử dụng `Ctrl+C` trong terminal nơi bạn đã chạy lệnh `vllm serve`.
* Để dừng ứng dụng Flask, sử dụng `Ctrl+C` trong terminal nơi bạn đã chạy lệnh `python app.py`.
* Để dừng Docker Compose, sử dụng lệnh `docker-compose down`.
## Tài liệu tham khảo
* [vllm Documentation](https://vllm.readthedocs.io/en/latest/)
* [Flask Documentation](https://flask.palletsprojects.com/)
* [Docker Documentation](https://docs.docker.com/)
* [OCR Model Documentation](https://huggingface.co/TienAnh/Finetune_OCR_1B)
* [Hugging Face Model Hub](https://huggingface.co/models)
* [CUDA Documentation](https://docs.nvidia.com/cuda/)

## Liên hệ
Nếu bạn có bất kỳ câu hỏi nào, vui lòng liên hệ với tôi qua email hoặc GitHub.