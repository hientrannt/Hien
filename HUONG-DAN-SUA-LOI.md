# HƯỚNG DẪN SỬA LỖI HIỂN THỊ LỊCH THÁNG

## Vấn đề
- Giờ bị hiển thị lặp lại 2 lần
- Không hiển thị địa điểm
- Cần định dạng màu sắc: Giờ (xanh, đậm), Nội dung (đen), Địa điểm (xám)

## Giải pháp

### Bước 1: Thêm CSS mới

Trong file HTML, tìm phần `<style>` và thêm CSS sau vào cuối (trước thẻ `</style>`):

```css
/* CSS MỚI CHO HIỂN THỊ SỰ KIỆN TRONG LỊCH THÁNG */
.grid-event-item {
  background: #fff;
  padding: 4px 6px;
  margin: 2px 0;
  border-radius: 4px;
  font-size: 0.75em;
  border-left: 3px solid rgba(33, 150, 243, 0.5);
  cursor: pointer;
  transition: all 0.14s ease;
  line-height: 1.3;
  box-shadow: none;
  text-align: left;
  width: 100%;
  max-width: 100%;
}

.grid-event-item:hover {
  background: linear-gradient(90deg, #e3f2fd, #f8f9fa);
  border-left-color: #2196F3;
  transform: translateX(2px);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* Định dạng giờ - MÀU XANH, TÔ ĐẬM */
.event-time {
  color: #1976D2;
  font-weight: 700;
  font-size: 0.95em;
  margin-right: 4px;
  display: inline-block;
}

/* Định dạng nội dung - MÀU ĐEN */
.event-content {
  color: #333;
  font-weight: 500;
  font-size: 0.9em;
  display: inline;
}

/* Định dạng địa điểm - MÀU XÁM */
.event-location {
  color: #666;
  font-weight: 400;
  font-size: 0.85em;
  font-style: italic;
  display: inline;
  margin-left: 3px;
}

.event-location:before {
  content: "📍 ";
  font-style: normal;
}
```

### Bước 2: Sửa JavaScript

Trong file HTML, tìm hàm `displayCalendarGrid`, sau đó tìm phần code:

```javascript
// 3. Sự kiện (nếu có và là tháng hiện tại)
var eventsCount = (eventsByDate[day] && eventsByDate[day].length) ? eventsByDate[day].length : 0;
if (isCurrentMonth && eventsCount > 0) {
```

**THAY THẾ** toàn bộ phần code từ dòng này đến hết khối `if` (khoảng 50 dòng) bằng code sau:

```javascript
// 3. Sự kiện - PHẦN SỬA ĐỔI CHÍNH
var eventsCount = (eventsByDate[day] && eventsByDate[day].length) ? eventsByDate[day].length : 0;
if (isCurrentMonth && eventsCount > 0) {
  // Hiển thị badge số lượng event nếu nhiều hơn 3
  if (eventsCount > 3) {
    calendarHTML += '<div class="events-count">+' + eventsCount + '</div>';
  }

  calendarHTML += '<div class="grid-day-events">';

  // Hiển thị tối đa 3 sự kiện
  eventsByDate[day].slice(0, 3).forEach(function(event) {
    var timeStr = event.time ? event.time.toString().trim() : '';
    var content = event.content || '';
    var location = event.location || '';

    // Format time để chỉ lấy HH:mm
    var displayTime = '';
    if (timeStr) {
      var timeMatch = timeStr.match(/^(\d{1,2}:\d{2})/);
      if (timeMatch) {
        displayTime = timeMatch[1];
      }
    }

    // Rút gọn content nếu quá dài
    var displayContent = content;
    if (displayContent.length > 30) {
      displayContent = displayContent.substring(0, 30) + '...';
    }

    // Tạo title cho tooltip
    var eventTitle = '';
    if (displayTime) eventTitle += displayTime + ' ';
    eventTitle += content;
    if (location) eventTitle += ' - ' + location;

    // Hiển thị: Giờ + Nội dung + Địa điểm (nếu có)
    calendarHTML += '<div class="grid-event-item" title="' + eventTitle.replace(/"/g, '&quot;') + '">';

    // 1. Hiển thị giờ (màu xanh, tô đậm)
    if (displayTime) {
      calendarHTML += '<span class="event-time">' + displayTime + '</span>';
    }

    // 2. Hiển thị nội dung (màu đen)
    if (displayContent) {
      calendarHTML += '<span class="event-content">' + displayContent.replace(/</g, '&lt;') + '</span>';
    }

    // 3. Hiển thị địa điểm (màu xám, có icon)
    if (location) {
      // Rút gọn location nếu quá dài
      var displayLocation = location;
      if (displayLocation.length > 20) {
        displayLocation = displayLocation.substring(0, 20) + '...';
      }
      calendarHTML += '<span class="event-location">' + displayLocation.replace(/</g, '&lt;') + '</span>';
    }

    calendarHTML += '</div>';
  });

  calendarHTML += '</div>';
}
```

### Bước 3: Kiểm tra và Deploy

1. Lưu file sau khi sửa
2. Deploy lên Google Apps Script
3. Kiểm tra lịch tháng - giờ sẽ chỉ hiển thị 1 lần với format:
   - **Giờ** (màu xanh #1976D2, tô đậm)
   - **Nội dung** (màu đen #333)
   - **📍 Địa điểm** (màu xám #666, italic)

## Kết quả mong đợi

Từ:
```
07:30
07:30
ĐỀ NGHỊ CẤP VỐN ngày 10/11/2025
```

Thành:
```
07:30 ĐỀ NGHỊ CẤP VỐN ngày 10/11/2025 📍 [Địa điểm nếu có]
```

Với:
- `07:30` - màu xanh, đậm
- `ĐỀ NGHỊ CẤP VỐN...` - màu đen
- `📍 [Địa điểm]` - màu xám, italic
