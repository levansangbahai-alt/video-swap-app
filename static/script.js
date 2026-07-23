// Elements
const uploadBox = document.getElementById('uploadBox');
const fileInput = document.getElementById('fileInput');
const selectBtn = document.getElementById('selectBtn');
const optionsSection = document.getElementById('optionsSection');
const progressSection = document.getElementById('progressSection');
const resultSection = document.getElementById('resultSection');
const errorSection = document.getElementById('errorSection');
const processBtn = document.getElementById('processBtn');
const resetBtn = document.getElementById('resetBtn');
const downloadBtn = document.getElementById('downloadBtn');
const newVideoBtn = document.getElementById('newVideoBtn');
const retryBtn = document.getElementById('retryBtn');
const fileName = document.getElementById('fileName');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const resultMessage = document.getElementById('resultMessage');
const errorMessage = document.getElementById('errorMessage');

let selectedFile = null;
let processedFilename = null;

// File selection
selectBtn.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) handleFileSelect(file);
});

// Drag and drop
uploadBox.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadBox.classList.add('dragover');
});

uploadBox.addEventListener('dragleave', () => {
    uploadBox.classList.remove('dragover');
});

uploadBox.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadBox.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file) handleFileSelect(file);
});

// Handle file selection
async function handleFileSelect(file) {
    const allowedFormats = ['video/mp4', 'video/x-msvideo', 'video/quicktime', 'video/x-matroska', 'video/x-flv', 'video/x-ms-wmv'];
    
    if (!allowedFormats.includes(file.type) && !file.name.match(/\.(mp4|avi|mov|mkv|flv|wmv)$/i)) {
        showError('Định dạng file không hỗ trợ. Vui lòng chọn: MP4, AVI, MOV, MKV, FLV hoặc WMV');
        return;
    }

    if (file.size > 500 * 1024 * 1024) {
        showError('File quá lớn (tối đa 500MB)');
        return;
    }

    selectedFile = file;
    fileName.textContent = file.name;
    
    // Upload file
    await uploadFile(file);
}

// Upload file
async function uploadFile(file) {
    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Upload failed');
        }

        // Show options
        document.querySelectorAll('section').forEach(s => s.style.display = 'none');
        optionsSection.style.display = 'block';
    } catch (error) {
        showError('Lỗi upload: ' + error.message);
    }
}

// Process video
processBtn.addEventListener('click', async () => {
    if (!selectedFile) return;

    const action = document.querySelector('input[name="action"]:checked').value;
    await processVideo(selectedFile.name, action);
});

async function processVideo(filename, action) {
    try {
        processBtn.disabled = true;
        document.querySelectorAll('section').forEach(s => s.style.display = 'none');
        progressSection.style.display = 'block';

        const response = await fetch('/api/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                filename: filename,
                action: action
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Processing failed');
        }

        const data = await response.json();
        processedFilename = data.output_filename;
        
        showSuccess(data.message, action);
    } catch (error) {
        showError('Lỗi xử lý: ' + error.message);
    } finally {
        processBtn.disabled = false;
    }
}

// Show sections
function showSuccess(message, action) {
    document.querySelectorAll('section').forEach(s => s.style.display = 'none');
    resultSection.style.display = 'block';
    resultMessage.textContent = `Video đã được ${action === 'swap' ? 'hoán đổi khuôn mặt' : 'làm mờ khuôn mặt'} thành công!`;
}

function showError(message) {
    document.querySelectorAll('section').forEach(s => s.style.display = 'none');
    errorSection.style.display = 'block';
    errorMessage.textContent = message;
}

// Download
downloadBtn.addEventListener('click', () => {
    if (processedFilename) {
        window.location.href = `/api/download/${processedFilename}`;
    }
});

// Reset
resetBtn.addEventListener('click', reset);
retryBtn.addEventListener('click', reset);
newVideoBtn.addEventListener('click', reset);

function reset() {
    selectedFile = null;
    processedFilename = null;
    fileInput.value = '';
    document.querySelectorAll('section').forEach(s => s.style.display = 'none');
    document.querySelector('.upload-section').style.display = 'block';
}

// Initial state
reset();
