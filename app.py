import os
import base64
from flask import Flask, request, render_template, jsonify
from openai import OpenAI
from werkzeug.utils import secure_filename
from PIL import Image


# Khởi tạo ứng dụng Flask
app = Flask(__name__)

# Cấu hình thư mục lưu trữ hình ảnh tạm thời
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Cấu hình client OpenAI 
BASE_URL = "https://c4fd-34-150-136-147.ngrok-free.app/v1" # Thay thế bằng được host bằng vLLMvLLM
API_KEY = "ahhihi"  # này k cần cũng đượcđược
MODEL_NAME = "TienAnh/Finetune_OCR_1B" # tên model đã host
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)

def resize_image(image_path):
    # Mở hình ảnh từ đường dẫn
    with Image.open(image_path) as img:
        # Kiểm tra và chuyển đổi chế độ nếu cần
        if img.mode == 'RGBA':
            # Tạo hình ảnh mới ở chế độ RGB với nền trắng
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[3])  # Sử dụng kênh alpha làm mask
            img = rgb_img
        elif img.mode != 'RGB':
            # Chuyển đổi các chế độ khác (như CMYK, L) sang RGB
            img = img.convert('RGB')

        # Resize ảnh về 448x448
        img = img.resize((448, 448))
        
        # Tạo đường dẫn cho ảnh đã resize
        resized_path = f"{os.path.splitext(image_path)[0]}_resized.jpg"
        
        # Lưu ảnh dưới dạng JPEG
        img.save(resized_path, format='JPEG', quality=95)  # Chỉ định format và chất lượng
    return resized_path

# Hàm mã hóa hình ảnh thành base64
def encode_image(image_path):
    # Mở và đọc file hình ảnh
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Route chính để hiển thị giao diện
@app.route('/')
def index():
    return render_template('index_new.html')

# Route xử lý tải lên hình ảnh và hỏi đáp
@app.route('/process', methods=['POST'])
def process_image():
    try:
        # Kiểm tra xem có hình ảnh được gửi lên không
        if 'image' not in request.files:
            return jsonify({'error': 'Không có hình ảnh được tải lên hoặc dán'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'Không có hình ảnh được chọn hoặc dán'}), 400

        # Lưu hình ảnh tạm thời
        filename = secure_filename(file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(image_path)
        print(f"Đã lưu hình ảnh tạm thời tại: {image_path}")

        # Lấy prompt từ form (mặc định hoặc do người dùng nhập)
        prompt = request.form.get('prompt', 'Trích xuất văn bản trên hình ảnh')
        resized_image_path = resize_image(image_path)

        # Mã hóa hình ảnh thành base64
        base64_image = encode_image(resized_image_path)

        # Gửi yêu cầu tới API
        response = client.chat.completions.create(
            # model=MODEL_NAME,
            model = client.models.list().data[0].id,
            max_tokens=4000,
            temperature=0.5,
            top_p=0.95,
            extra_body={
                "skip_special_tokens": False,
                "spaces_between_special_tokens": False,
                # "use_beam_search": True,
            },
            messages=[
                {
                    "role": "system",
                    "content": "Bạn là một mô hình trí tuệ nhân tạo đa phương thức Tiếng Việt có tên gọi là Vintern, được phát triển bởi người Việt. Bạn là một trợ lý trí tuệ nhân tạo hữu ích và không gây hại."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "<image>\n"+prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
        )

        # Lấy câu trả lời từ API
        answer = response.choices[0].message.content
        print(answer)

        with open('response.md', 'w', encoding='utf-8') as f:
            f.write(answer)

        # Trả về kết quả và đường dẫn hình ảnh
        return jsonify({
            'answer': answer,
            'image_url': f'/static/uploads/{filename}'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route để xóa hình ảnh cũ
@app.route('/clear', methods=['POST'])
def clear():
    try:
        for file in os.listdir(app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        return jsonify({'message': 'Đã xóa hình ảnh cũ'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)