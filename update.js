const fs = require('fs');

async function main() {
    console.log("Đang tiến hành cập nhật dữ liệu thị trường...");

    // Ở đây bạn có thể viết logic fetch dữ liệu từ một API công khai hoặc trang nguồn
    // Hoặc giả lập cập nhật lại mốc thời gian và giá đạn mới nhất:
    
    const rawData = fs.readFileSync('data.json', 'utf8');
    let data = JSON.parse(rawData);

    // Cập nhật lại thời gian chạy action mới nhất
    const now = new Date();
    data.last_updated = `${now.getFullYear()}/${String(now.getMonth() + 1).padStart(2, '0')}/${String(now.getDate()).padStart(2, '0')} ${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;

    // Lưu lại file data.json
    fs.writeFileSync('data.json', JSON.stringify(data, null, 2), 'utf8');
    console.log("Cập nhật file data.json thành công!");
}

main();
