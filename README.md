# 🚀 CP Testcase Generator

Hệ thống pipeline tự động sinh **testcase generator** cho các bài toán Competitive Programming, sử dụng AI để phân tích đề bài và tạo mã C++ sinh test.

---

## ✨ Tính năng nổi bật

- 🔍 **Phân tích tự động** đề bài (statement) và solution mẫu  
- 🧠 **Sinh mã C++ generator** hoàn toàn tự động  
- 📦 Hỗ trợ nhiều loại test:
  - Small tests  
  - Random tests  
  - Edge cases  
  - Stress tests  
- ⚙️ **Tích hợp GitHub Actions** để chạy pipeline tự động  
- 📁 Xuất testcase dưới dạng thư mục `input/output` hoặc file `.zip`  

---

## 🏗️ Cấu trúc thư mục



```
cp-testcase-generator/
├── data/
│   └── sample_generator_code.txt
│   └── libary_code.txt (optional)
│   └── problem_data.jsonl:
│       └── field: statement, input, output, code
├── generators/            # Test generators will be created
│   └── problem_id
│       └── generator_code.cpp
│       └── testcases
│       └── testcase.zip
├── migrate/            # Migrate some data from database
├── src/
│   └── testcase_gen.py # Main file prompt AI to generate code 
│   └── run.cpp # Run code to generate testcase
```

## 🚀 Cách sử dụng

**Bước 1: Hoàn thành các folder structure và rename theo tên file trong testcase.cpp**

**Bước 2: Đưa dữ liệu vào .env**


**Bước 3. Cài đặt thư viện**
```bash
pip install -r requirements.txt
```

**Bước 4: python src/testcase_gen.py**

## 📚 Ví dụ

Xem folder `problems/example_sum` để tham khảo cách setup một bài toán mẫu.

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Hãy tạo issue hoặc pull request.

## 📄 License

MIT License

---

Made with ❤️ and AI
