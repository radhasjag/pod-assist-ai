let isRecording = false;
let startTime;
let timerInterval;

const startStopBtn = document.getElementById('startStopBtn');
const timer = document.getElementById('timer');
const transcription = document.getElementById('transcription');
const facts = document.getElementById('facts');
const topics = document.getElementById('topics');
const suggestions = document.getElementById('suggestions');

startStopBtn.addEventListener('click', toggleRecording);

function toggleRecording() {
    if (isRecording) {
        stopRecording();
    } else {
        startRecording();
    }
}

function startRecording() {
    isRecording = true;
    startStopBtn.textContent = 'Stop Recording';
    startTime = Date.now();
    updateTimer();
    timerInterval = setInterval(updateTimer, 1000);
    
    // Here we would typically start the actual audio recording
    // For this example, we'll simulate it with setInterval
    simulateAudioProcessing();
}

function stopRecording() {
    isRecording = false;
    startStopBtn.textContent = 'Start Recording';
    clearInterval(timerInterval);
}

function updateTimer() {
    const elapsedTime = Date.now() - startTime;
    const seconds = Math.floor(elapsedTime / 1000) % 60;
    const minutes = Math.floor(elapsedTime / 60000);
    timer.textContent = `${padZero(minutes)}:${padZero(seconds)}`;
}

function padZero(num) {
    return num.toString().padStart(2, '0');
}

function simulateAudioProcessing() {
    setInterval(() => {
        if (isRecording) {
            const audioData = 'Simulated audio data';
            processAudio(audioData);
        }
    }, 5000);  // Process every 5 seconds
}

function processAudio(audioData) {
    fetch('/process_audio', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ audio: audioData }),
    })
    .then(response => response.json())
    .then(data => {
        updateUI(data);
    })
    .catch(error => console.error('Error:', error));
}

function updateUI(data) {
    transcription.textContent = data.transcription;
    facts.innerHTML = '<h3>Fact Checks:</h3>' + data.facts.map(fact => `<p>${fact}</p>`).join('');
    topics.innerHTML = '<h3>Current Topics:</h3>' + data.topics.map(topic => `<p>${topic}</p>`).join('');
    suggestions.innerHTML = '<h3>Suggestions:</h3>' + data.suggestions.map(suggestion => `<p>${suggestion}</p>`).join('');
}
