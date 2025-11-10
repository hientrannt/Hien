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

    // Hiển thị: Giờ : Nội dung
    //          Địa điểm
    // Ví dụ: 07:30 : ĐỀ NGHỊ CẤP VỐN ngày 10/11/2025
    //        Truy cập BFO:Link 02.Quản Lý Tài Chánh/36. Quản Lý Cấp Vốn/01. Yêu Cầu Cấp Vốn
    calendarHTML += '<div class="grid-event-item" title="' + eventTitle.replace(/"/g, '&quot;') + '">';

    // Dòng 1: Giờ : Nội dung
    var firstLine = '';

    // 1. Hiển thị giờ (màu xanh, tô đậm)
    if (displayTime) {
      firstLine += '<span class="event-time">' + displayTime + '</span>';
      firstLine += '<span class="event-separator"> : </span>';
    }

    // 2. Hiển thị nội dung đầy đủ (màu đen)
    if (displayContent) {
      firstLine += '<span class="event-content">' + displayContent.replace(/</g, '&lt;') + '</span>';
    }

    calendarHTML += '<div>' + firstLine + '</div>';

    // Dòng 2: Địa điểm (nếu có)
    if (displayLocation) {
      calendarHTML += '<div><span class="event-location">' + displayLocation.replace(/</g, '&lt;') + '</span></div>';
    }

    calendarHTML += '</div>';
  });

  calendarHTML += '</div>';
}
