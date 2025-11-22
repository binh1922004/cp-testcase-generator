# 🚀 CP Testcase Generator

Pipeline tự động sử dụng AI để sinh test generator cho các bài toán Competitive Programming.

## 📋 Tính năng

- ✅ Tự động phân tích đề bài (statement) và solution
- ✅ Sinh test generator code (C++) tự động
- ✅ Hỗ trợ nhiều loại test: small, random, edge cases, stress tests
- ✅ GitHub Actions workflow tự động
- ✅ Format output: folders chứa inp/out files

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

Bước 1: Hoàn thành các folder structure và rename theo tên file trong testcase.cpp
Bước 2: Đưa dữ liệu vào .env
Bước 3: pip install -r requirements.txt
Bước 4: python src/testcase_gen.py

## 📚 Ví dụ

Xem folder `problems/example_sum` để tham khảo cách setup một bài toán mẫu.

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Hãy tạo issue hoặc pull request.

## 📄 License

MIT License

---

Made with ❤️ and AI
