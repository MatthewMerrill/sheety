let video;
let stream;
let canvas;

function captureFrame() {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    return context.getImageData(0, 0, canvas.width, canvas.height);
}

function captureFrameBlob() {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    return canvas.toBlob();
}

function lookForPen() {
    const [x, y] = findPen(captureFrame());
    blob.style.display = 'block';
    blob.style.left = x - blob.style.width/2;
    blob.style.top = y - blob.style.height/2;
}

function findPen(frame) {
    const {data, width, height} = frame;
    for (let i = 0; i < width*height; i++) {
        const r = data[i*4];
        const g = data[i*4+1];
        const b = data[i*4+2];
        if (g - r > 30 && g - b > 30)
            return [i % width, Math.floor(i / width)]
    }
    return [-1, -1];
}

function doThreshold(frame, threshold) {
    const {data, width, height} = frame;
    const newFrame = new ImageData(width,height);
    const newData = newFrame.data;
    for (let i = 0; i < width*height; i++) {
        const r = data[i*4];
        const g = data[i*4+1];
        const b = data[i*4+2];
        let v = (r + g + b) / 3;
        if (v > threshold)
            v = 255;
        else
            v = 0;
        newData[i*4]=newData[i*4+1]=newData[i*4+2]=v;
        newData[i*4+3]=255;
    }
    return newFrame;
}

let thresholdPreviewTimeout;
function onThresholdChange(event) {
    const threshold = event.target.value;
    const thresholdImageData = doThreshold(captureFrame(), threshold);
    canvas.width = thresholdImageData.width;
    canvas.height = thresholdImageData.height;
    const context = canvas.getContext('2d');
    context.putImageData(thresholdImageData, 0, 0);
    thresholdPreview.src = canvas.toDataURL();
    thresholdPreview.style.display = 'block';
    if (thresholdPreviewTimeout)
        clearTimeout(thresholdPreviewTimeout)
    thresholdPreviewTimeout = setTimeout(function() {
        thresholdPreview.style.display = 'none';
        thresholdPreviewTimeout = null;
    }, 1000);
}

async function ligmaMediaRecorder() {
    const frame = captureFrameBlob();

    downloadButton.innerText = 'asdf';
    downloadButton.href = URL.createObjectURL(frame);
    downloadButton.download = true;
    document.body.appendChild(downloadButton);

    const formdata = new FormData();
    formdata.set('frame', frame);
    formdata.set('threshold', threshold.value);

    const response = await fetch('/video', {
        method: 'POST',
        body: formdata,
    });
    alert(JSON.stringify(await response.json()))
}

async function setupVideo() {
    video = document.createElement('video');
    stream = await navigator.mediaDevices.getUserMedia({video: {
      video: {
        width: { ideal: 4096 },
          height: { ideal: 2160 } 
        },
        facingMode: 'environment'}
    });
    video.srcObject = stream;
    video.autoplay = true;
    video.onplay = function() {
        video.onplay = null;
        setInterval(lookForPen, 33);
    };
    document.body.appendChild(video);
    canvas = document.createElement('canvas');
    goButton.style.display = 'block';
    goButton.onclick = function() {
        ligmaMediaRecorder().catch(console.error);
    };
    threshold.oninput = onThresholdChange;
}

setupVideo().catch(console.error);
