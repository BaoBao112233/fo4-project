# FIFA Online 4 Event Tracker

Ứng dụng AI tự động theo dõi và cập nhật các sự kiện trong trò chơi FIFA Online 4.

## Tính năng

- Tự động thu thập thông tin sự kiện từ trang web chính thức của FIFA Online 4
- Tạo tóm tắt về các sự kiện mới
- Lên lịch cập nhật hàng ngày
- Dễ dàng mở rộng với các công cụ và agent mới

## Cài đặt

Cài đặt các dependency:

```bash
pip install -e .
```

Hoặc sử dụng Poetry:

```bash
poetry install
```

## Cấu hình

Tạo file `.env` trong thư mục gốc và thêm các biến môi trường sau:

```
OPENAI_API_KEY=your_openai_api_key
```

## Sử dụng

Khởi động agent:

```bash
python -m fo4.main
```

Hoặc sử dụng script đã cấu hình trong Poetry:

```bash
poetry run start
```

## Kiến trúc

- `agents/`: Chứa các agent AI, như Fo4EventTrackerAgent
- `tools/`: Chứa các công cụ được sử dụng bởi agent, như Fo4EventScraperTool

## Phát triển

Chạy kiểm thử:

```bash
pytest
```

## Giấy phép

[MIT](LICENSE) 