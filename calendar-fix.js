// PHẦN CODE SỬA ĐỔI CHO HÀM displayCalendarGrid
// Tìm và thay thế phần code hiển thị sự kiện trong hàm renderCalendarGrid()

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

    // Hiển thị đầy đủ content và location - KHÔNG rút gọn
    var displayContent = content;
    var displayLocation = location;

    // Tạo title cho tooltip
    var eventTitle = '';
    if (displayTime) eventTitle += displayTime + ' --> ';
    eventTitle += content;
    if (location) eventTitle += ' 📍 ' + location;

    // Hiển thị: Giờ --> Nội dung 📍 Địa điểm
    calendarHTML += '<div class="grid-event-item" title="' + eventTitle.replace(/"/g, '&quot;') + '">';

    // 1. Hiển thị giờ (màu xanh, tô đậm) với mũi tên
    if (displayTime) {
      calendarHTML += '<span class="event-time">' + displayTime + ' → </span>';
    }

    // 2. Hiển thị nội dung đầy đủ (màu đen)
    if (displayContent) {
      calendarHTML += '<span class="event-content">' + displayContent.replace(/</g, '&lt;') + '</span>';
    }

    // 3. Hiển thị địa điểm đầy đủ (màu xám, có icon 📍)
    if (displayLocation) {
      calendarHTML += '<span class="event-location">' + displayLocation.replace(/</g, '&lt;') + '</span>';
    }

    calendarHTML += '</div>';
  });

  calendarHTML += '</div>';
}
