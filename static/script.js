"use strict";

/* ====================================================
   Global Variables for Attached Files
======================================================= */
let attachedDocument = null;
let attachedSignature = null;
let currentFileType = null;

function updateAttachedFileUI() {
    let container = document.getElementById('attached-files-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'attached-files-container';
        container.classList.add('attached-files-container'); // For CSS flex styling
        // Insert container just below the controls container
        const controlsContainer = document.getElementById('controls-container');
        controlsContainer.insertAdjacentElement('afterend', container);
    }
    // Clear container content
    container.innerHTML = '';

    // Documents box
    const documentsBox = document.createElement('div');
    documentsBox.id = 'documents-box';
    documentsBox.classList.add('attached-file-box');
    documentsBox.innerHTML = '<h4>Documents</h4>';
    if (attachedDocument) {
        documentsBox.innerHTML += `
            <div class="file-info">
                <span class="file-name">${attachedDocument.name}</span>
                <button class="remove-btn" data-type="document">Remove</button>
            </div>
        `;
    }
    container.appendChild(documentsBox);

    // Signature box
    const signatureBox = document.createElement('div');
    signatureBox.id = 'signature-box';
    signatureBox.classList.add('attached-file-box');
    signatureBox.innerHTML = '<h4>Signature</h4>';
    if (attachedSignature) {
        signatureBox.innerHTML += `
            <div class="file-info">
                <span class="file-name">${attachedSignature.name}</span>
                <button class="remove-btn" data-type="signature">Remove</button>
            </div>
        `;
    }
    container.appendChild(signatureBox);

    // Attach remove event listeners
    const removeButtons = container.querySelectorAll('.remove-btn');
    removeButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const type = btn.getAttribute('data-type');
            if (type === 'document') {
                attachedDocument = null;
            } else if (type === 'signature') {
                attachedSignature = null;
            }
            updateAttachedFileUI();
            // Also clear file input value
            document.getElementById('file-input').value = '';
        });
    });

    // If both boxes are empty, remove the container from the DOM
    if (!attachedDocument && !attachedSignature) {
        if (container.parentNode) {
            container.parentNode.removeChild(container);
        }
    }
}

function showFileTypeSelectionPopup() {
    // Create overlay div and use a CSS class instead of inline styles
    const overlay = document.createElement('div');
    overlay.id = 'file-type-popup';
    overlay.classList.add('file-type-popup-overlay');

    // Create popup content div with a CSS class for styling
    const popup = document.createElement('div');
    popup.classList.add('file-type-popup-content');

    const message = document.createElement('p');
    message.textContent = 'What type of file are you attaching?';
    message.style.marginTop = '30px';
    popup.appendChild(message);

    // Create a close button (cross symbol) in the upper right corner using a CSS class
    const closeButton = document.createElement('span');
    closeButton.innerHTML = '&times;';
    closeButton.classList.add('file-type-popup-close');
    popup.appendChild(closeButton);

    // Create buttons with CSS classes for styling
    const docButton = document.createElement('button');
    docButton.textContent = 'Document';
    docButton.classList.add('popup-button');

    const signButton = document.createElement('button');
    signButton.textContent = 'Signature';
    signButton.classList.add('popup-button');

    popup.appendChild(docButton);
    popup.appendChild(signButton);

    overlay.appendChild(popup);
    document.body.appendChild(overlay);

    // Function to remove popup and cleanup event listeners
    const removePopup = () => {
        if (overlay && overlay.parentNode) {
            overlay.parentNode.removeChild(overlay);
        }
        document.removeEventListener('keydown', handleEscape);
    };

    // Event listener for Escape key
    const handleEscape = (event) => {
        if (event.key === "Escape") {
            removePopup();
        }
    };
    document.addEventListener('keydown', handleEscape);

    // Event listeners for buttons
    docButton.addEventListener('click', () => {
        currentFileType = 'document';
        // Set file input accept for Document: PDF and common image formats
        document.getElementById('file-input').setAttribute('accept', 'application/pdf,image/jpeg,image/png,image/gif,image/bmp,image/tiff');
        removePopup();
        document.getElementById('file-input').click();
    });
    signButton.addEventListener('click', () => {
        currentFileType = 'signature';
        // Set file input accept for Signature: only PNG
        document.getElementById('file-input').setAttribute('accept', 'image/png');
        removePopup();
        document.getElementById('file-input').click();
    });
    closeButton.addEventListener('click', removePopup);
}

var analyser = null;
var firstRun = true;
var running = false;

const oscElem = document.querySelector('#oscilloscope');
const svgElem = document.querySelector('#graph');
const waveElem = document.querySelector('#wave');

const playBtn = document.querySelector('#play-btn');
const stopBtn = document.querySelector('#stop-btn');

playBtn.addEventListener('click', (e) => {
    e.preventDefault();
    running = true;
    playBtn.style.backgroundColor = "#E50046"; // Change play button color when pressed
    if (firstRun)
        init();
    else
        render();
});

stopBtn.addEventListener('click', (e) => {
    e.preventDefault();
    running = false;
    playBtn.style.backgroundColor = getComputedStyle(document.body).getPropertyValue("--bgcolor");
});

const modeBtn = document.querySelector('#light-mode-checkbox');
modeBtn.addEventListener('change', (e) => {
    const body = document.body;
    const fgColor = getComputedStyle(body).getPropertyValue('--fgcolor');
    const bgColor = getComputedStyle(body).getPropertyValue('--bgcolor');
    body.style.setProperty('--fgcolor', bgColor);
    body.style.setProperty('--bgcolor', fgColor);
    if (!running) {
        playBtn.style.backgroundColor = getComputedStyle(document.body).getPropertyValue("--bgcolor");
    }
});

function init() {
    firstRun = false;
    initMediaDevices();

    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    if (audioCtx.state === "suspended") {
        audioCtx.resume();
    }

    analyser = audioCtx.createAnalyser();
    analyser.fftSize = 2048;

    if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                const source = audioCtx.createMediaStreamSource(stream);
                source.connect(analyser);
            })
            .catch(e => {
                setErrorMessage("Access to the microphone failed. (" + e.name + ": " + e.message + ")");
            });
    } else {
        setErrorMessage('getUserMedia() not supported on your browser!');
    }
    render();
}

function render() {
    var bufferLength = analyser.frequencyBinCount;
    var dataArray = new Uint8Array(bufferLength);
    analyser.getByteTimeDomainData(dataArray);

    const clientWidth = svgElem.clientWidth;
    const clientHeight = svgElem.clientHeight;
    waveElem.points.clear();

    for (let i = 0; i < bufferLength; i++) {
        const value = dataArray[i];
        let point = waveElem.points.appendItem(svgElem.createSVGPoint());
        point.x = i * (clientWidth / bufferLength);
        point.y = value * (clientHeight / 256);
    }
    if (running)
        requestAnimationFrame(render);
}

function setErrorMessage(msg) {
    const msgElem = document.querySelector('#message');
    msgElem.innerText = msg;
    if (msg.length > 0)
        msgElem.style.removeProperty('display');
    else
        msgElem.style.display = 'none';
}

function initMediaDevices() {
    if (navigator.mediaDevices === undefined) {
        navigator.mediaDevices = {};
    }
    if (navigator.mediaDevices.getUserMedia === undefined) {
        navigator.mediaDevices.getUserMedia = function (constraints) {
            var getUserMedia = navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
            if (!getUserMedia) {
                return Promise.reject(new Error('getUserMedia() is not implemented in this browser'));
            }
            return new Promise(function (resolve, reject) {
                getUserMedia.call(navigator, constraints, resolve, reject);
            });
        }
    }
}

window.addEventListener('resize', (e) => {
    waveElem.points.clear();
});



document.addEventListener('DOMContentLoaded', () => {
    const chatInput = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendBtn');
    const chatFooter = document.querySelector('.chat-footer');
    const container = document.getElementById('container');

    let resizeTimeout;

    function autoResize() {
        if (resizeTimeout) clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            chatInput.style.height = 'auto';
            const maxHeight = 200;
            const contentHeight = chatInput.scrollHeight;
            if (contentHeight <= maxHeight) {
                chatInput.style.height = contentHeight + 'px';
                chatInput.style.overflowY = 'hidden';
            } else {
                chatInput.style.height = maxHeight + 'px';
                chatInput.style.overflowY = 'auto';
            }
            container.style.paddingBottom = chatFooter.offsetHeight + "px";
        }, 50);
    }

    chatInput.addEventListener('input', autoResize);
    autoResize();

    chatInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    sendBtn.addEventListener('click', sendMessage);

    function sendMessage() {
        if (!attachedSignature) {
            const notification = document.getElementById('processing-notification');
            notification.innerText = "You should attach a signature by clicking the Upload File button.";
            notification.style.display = 'block';
            setTimeout(() => {
                notification.style.display = 'none';
                notification.innerText = "Audio is processing...";
            }, 3000);
            return;
        }
        const message = chatInput.value.trim();
        const formData = new FormData();

        // Append text if available
        if (message) {
            formData.append('user_text', message);
        }

        // Append attached files if they exist
        if (attachedDocument) {
            formData.append('document', attachedDocument);
        }
        if (attachedSignature) {
            formData.append('signature', attachedSignature);
        }
        // Show notification "PDF file crafting..." as soon as submit is clicked
        const notification = document.getElementById('processing-notification');
        notification.innerText = "PDF file crafting...";
        notification.style.display = 'block';

        // Only send if there's any content
        if (message || attachedDocument || attachedSignature) {
            fetch('/submit', {
                method: 'POST',
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    console.log('Server responded with:', data);
                    if (data.download_url) {
                        // Automatically open the URL in a new tab
                        window.open(data.download_url, '_blank');
                    }
                    // Hide notification after receiving response
                    notification.style.display = 'none';
                })
                .catch(error => {
                    console.error('Error sending message:', error);
                    notification.style.display = 'none';
                });

            // Clear input and attached files
            chatInput.value = '';
            attachedDocument = null;
            attachedSignature = null;
            document.getElementById('file-input').value = '';
            updateAttachedFileUI();
            chatInput.style.height = 'auto';
            autoResize();
        }
    }
});



let mediaRecorder;
let audioChunks = [];

document.getElementById('play-btn').addEventListener('click', async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.start();
        audioChunks = [];

        mediaRecorder.addEventListener("dataavailable", event => {
            if (event.data.size > 0) {
                audioChunks.push(event.data);
            }
        });

        mediaRecorder.addEventListener("stop", async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const formData = new FormData();
            // Append the recording file with a descriptive filename
            formData.append('audio', audioBlob, 'recording.wav');

            // Read the selected option from the dropdown and include it in the request.
            const selectedOption = document.getElementById('recording-option').value;
            formData.append('option', selectedOption);

            try {
                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                const notification = document.getElementById('processing-notification');

                if (response.ok) {
                    const chatInputElem = document.getElementById('chatInput');
                    chatInputElem.value += data.transcript;
                    chatInputElem.dispatchEvent(new Event('input'));
                } else {
                    console.error(data.error || 'Error processing file');
                }

                // Hide the notification immediately after processing the response
                if (notification) {
                    notification.style.display = 'none';
                }
            } catch (error) {
                console.error('Error uploading audio:', error);
            }
        });

        document.getElementById('play-btn').disabled = true;
        document.getElementById('stop-btn').disabled = false;
    } catch (err) {
        console.error('Error accessing microphone:', err);
        alert('Could not access your microphone.');
    }
});

document.getElementById('stop-btn').addEventListener('click', () => {
    const notification = document.getElementById('processing-notification');
    if (notification) {
        notification.style.display = 'block';
    }
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
    }
    document.getElementById('play-btn').disabled = false;
    document.getElementById('stop-btn').disabled = true;
});


// When the Dropbox button is clicked, show the file type selection popup
document.getElementById('dropbox-button').addEventListener('click', function () {
    showFileTypeSelectionPopup();
});

// When a file is selected, validate and attach it based on currentFileType
document.getElementById('file-input').addEventListener('change', function (event) {
    const file = event.target.files[0];
    if (file) {
        const fileName = file.name.toLowerCase();
        if (currentFileType === 'document') {
            const allowedExtensions = ['pdf', 'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff'];
            const ext = fileName.split('.').pop();
            if (allowedExtensions.indexOf(ext) === -1) {
                console.error('Selected file is not an allowed document type.');
                alert('Please select a PDF or common image file for a document.');
                return;
            }
            attachedDocument = file;
        } else if (currentFileType === 'signature') {
            if (!fileName.endsWith('.png')) {
                console.error('Selected file is not a PNG for signature.');
                alert('Please select a PNG file for a signature.');
                return;
            }
            attachedSignature = file;
        }
        updateAttachedFileUI();
    }
});