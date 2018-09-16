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

function lookForPen() {
    const [x, y] = findPen(captureFrame());
    console.log(x, y)
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

async function ligmaMediaRecorder() {
    const recorder = new MediaRecorder(stream, {mimeType: 'video/webm'}); // consider setting bitrate
    const data = [];
    recorder.ondataavailable = (event) => {
        data.push(event.data);
        console.log('data!');
    };
    recorder.onerror = console.error;
    recorder.start();
    console.log('start recording');
    await new Promise(resolve => setTimeout(resolve, 1000));
    console.log(recorder.state);
    const stopped = new Promise((resolve, reject) => {
        recorder.onstop = resolve;
        recorder.onerror = reject;
    });
    recorder.stop();
    await stopped;
    console.log('done recording');
    const webm = new Blob(data, {type: 'video/webm'});

    return;

    const downloadButton = document.createElement('a');
    downloadButton.href = URL.createObjectURL(webm);
    downloadButton.download = 'fucl.webm';
    document.body.appendChild(downloadButton);
}

async function setupVideo() {
    video = document.createElement('video');
    stream = await navigator.mediaDevices.getUserMedia({video: {facingMode: 'environment'}});
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
        console.log('begin ligma');
        ligmaMediaRecorder().catch(console.error);
    };
}

setupVideo().catch(console.error);
