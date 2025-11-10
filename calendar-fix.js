// PHẦN CODE SỬA ĐỔI CHO HÀM displayCalendarGrid
// Tìm và thay thế phần code hiển thị sự kiện trong hàm renderCalendarGrid()

// 3. Sự kiện - PHẦN SỬA ĐỔI CHÍNH
var eventsCount = (eventsByDate[day] && eventsByDate[day].length) ? eventsByDate[day].length : 0;
if (isCurrentMonth && eventsCount > 0) {
  calendarHTML += '<div class="grid-day-events">';

  // Hiển thị TẤT CẢ sự kiện (không giới hạn)
  eventsByDate[day].forEach(function(event) {
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
    if (displayTime) eventTitle += displayTime + ' : ';
    eventTitle += content;
    if (location) eventTitle += ' - ' + location;

    // Hiển thị: Giờ : Nội dung - Địa điểm
    // Ví dụ: 16:55 : Đón SoMin và Soda - Mầm non Lộc Thọ 1
    calendarHTML += '<div class="grid-event-item" title="' + eventTitle.replace(/"/g, '&quot;') + '">';

    var eventLine = '';

    // 1. Hiển thị giờ (màu xanh, tô đậm)
    if (displayTime) {
      eventLine += '<span class="event-time">' + displayTime + '</span>';
      eventLine += '<span class="event-separator"> : </span>';
    }

    // 2. Hiển thị nội dung đầy đủ (màu đen)
    if (displayContent) {
      eventLine += '<span class="event-content">' + displayContent.replace(/</g, '&lt;') + '</span>';
    }

    // 3. Hiển thị địa điểm đầy đủ (màu xám)
    if (displayLocation) {
      eventLine += '<span class="event-separator"> - </span>';
      eventLine += '<span class="event-location">' + displayLocation.replace(/</g, '&lt;') + '</span>';
    }

    calendarHTML += eventLine;
    calendarHTML += '</div>';
  });

  calendarHTML += '</div>';
}
