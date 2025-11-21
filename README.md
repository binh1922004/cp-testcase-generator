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
├── problems/              # Đặt bài toán vào đây
│   ├── example_problem/
│   │   ├── statement.md   # Đề bài
│   │   ├── solution.cpp   # Lời giải
│   │   └── config.json    # Cấu hình (optional)
│   └── ...
├── generators/            # Test generators được sinh ra
│   └── example_problem_gen.cpp
├── testcases/            # Testcases được sinh ra
│   └── example_problem/
│       ├── test_001/
│       │   ├── inp
│       │   └── out
│       └── test_002/
│           ├── inp
│           └── out
├── scripts/
│   ├── generate_testgen.py    # Script sinh generator
│   └── run_generator.py       # Script chạy generator
├── templates/
│   └── generator_template.cpp # Template mẫu
└── .github/
    └── workflows/
        └── auto-generate.yml  # GitHub Actions
```

## 🚀 Cách sử dụng

### Option 1: Tự động với GitHub Actions

1. Tạo folder mới trong `problems/`:
```bash
mkdir -p problems/your_problem
```

2. Thêm các files:
- `statement.md`: Đề bài
- `solution.cpp`: Lời giải của bạn
- `config.json` (optional): Cấu hình

3. Push lên GitHub:
```bash
git add problems/your_problem
git commit -m "Add new problem: your_problem"
git push
```

4. GitHub Actions sẽ tự động:
- Phân tích đề bài và solution
- Sinh test generator
- Tạo Pull Request để review

### Option 2: Chạy local

```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Sinh test generator
python scripts/generate_testgen.py -p problems/your_problem

# Compile và chạy generator
python scripts/run_generator.py -p your_problem -n 10
```

## 📝 Format files

### statement.md
```markdown
# Tên bài toán

## Đề bài
Mô tả bài toán...

## Input
Format input...

## Output
Format output...

## Constraints
- 1 ≤ n ≤ 10^5
- 1 ≤ a[i] ≤ 10^9

## Example
Input:
```
3
1 2 3
```

Output:
```
6
```
```

### config.json (optional)
```json
{
  "num_tests": 20,
  "test_types": {
    "small": 5,
    "random": 10,
    "edge": 3,
    "stress": 2
  },
  "constraints": {
    "n_max": 100000,
    "value_max": 1000000000
  }
}
```

## 🔧 Setup GitHub Actions

Repository đã được cấu hình sẵn GitHub Actions. Bạn cần:

1. Vào **Settings** → **Actions** → **General**
2. Cho phép **Read and write permissions**
3. Đảm bảo **Allow GitHub Actions to create and approve pull requests** được bật

## 📚 Ví dụ

Xem folder `problems/example_sum` để tham khảo cách setup một bài toán mẫu.

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Hãy tạo issue hoặc pull request.

## 📄 License

MIT License

---

Made with ❤️ and AI
