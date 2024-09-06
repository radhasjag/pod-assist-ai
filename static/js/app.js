let isRecording = false;
let startTime;
let timerInterval;

const startStopBtn = document.getElementById('startStopBtn');
const timer = document.getElementById('timer');
const transcription = document.getElementById('transcription');
const sentiment_emotion = document.getElementById('sentiment_emotion');
const conversation_dynamics = document.getElementById('conversation_dynamics');
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
    transcription.innerHTML = `<h2><span class="icon icon-mic"></span>Transcription</h2><p>${data.transcription}</p>`;
    
    const sentimentAnalysis = data.conversation_analysis.sentiment_analysis;
    sentiment_emotion.innerHTML = `
        <h2><span class="icon icon-sentiment"></span>Sentiment and Emotion Analysis</h2>
        <p>TextBlob Sentiment: ${sentimentAnalysis.textblob_sentiment.toFixed(2)}</p>
        <p>Hugging Face Sentiment: ${sentimentAnalysis.huggingface_sentiment.label} (${sentimentAnalysis.huggingface_sentiment.score.toFixed(2)})</p>
        <p>GPT Analysis:</p>
        <ul>
            <li>Overall Sentiment: ${sentimentAnalysis.gpt_analysis.overall_sentiment}</li>
            <li>Emotions: ${sentimentAnalysis.gpt_analysis.emotions}</li>
        </ul>
        <p>Explanation: ${sentimentAnalysis.gpt_analysis.explanation}</p>
    `;

    const dynamicsAnalysis = data.conversation_analysis.dynamics_analysis;
    conversation_dynamics.innerHTML = `
        <h2><span class="icon icon-dynamics"></span>Conversation Dynamics</h2>
        <h3>Basic Metrics:</h3>
        <ul>
            <li>Turn-taking: ${dynamicsAnalysis.basic_metrics.turn_taking} turns</li>
            <li>Average Sentence Length: ${dynamicsAnalysis.basic_metrics.avg_sentence_length.toFixed(2)} words</li>
            <li>Average Word Length: ${dynamicsAnalysis.basic_metrics.avg_word_length.toFixed(2)} characters</li>
        </ul>
        <h3>GPT Analysis:</h3>
        <ul>
            <li>Turn-taking: ${dynamicsAnalysis.gpt_analysis.turn_taking}</li>
            <li>Interruptions: ${dynamicsAnalysis.gpt_analysis.interruptions}</li>
            <li>Topic Coherence: ${dynamicsAnalysis.gpt_analysis.topic_coherence}</li>
            <li>Flow: ${dynamicsAnalysis.gpt_analysis.flow}</li>
        </ul>
        <p>Explanation: ${dynamicsAnalysis.gpt_analysis.explanation}</p>
    `;

    const topicAnalysis = data.conversation_analysis.topic_analysis;
    topics.innerHTML = `
        <h2><span class="icon icon-topic"></span>Topic Analysis</h2>
        <h3>LDA Topics:</h3>
        <ul>
            ${topicAnalysis.lda_topics.map(topic => `<li>Topic ${topic.topic_id}: ${topic.keywords}</li>`).join('')}
        </ul>
        <h3>Zero-shot Classification:</h3>
        <ul>
            ${topicAnalysis.zero_shot_classification.labels.map((label, index) => 
                `<li>${label}: ${topicAnalysis.zero_shot_classification.scores[index].toFixed(2)}</li>`
            ).join('')}
        </ul>
    `;

    facts.innerHTML = '<h2><span class="icon icon-fact"></span>Fact Checks</h2>' + 
        data.facts.map(fact => `
            <div class="fact">
                <p><strong>Claim:</strong> ${fact.claim}</p>
                <p><strong>Accuracy:</strong> ${fact.accuracy}</p>
                <p><strong>Evidence:</strong> ${fact.evidence}</p>
                <p><strong>Importance:</strong> ${fact.importance}</p>
            </div>
        `).join('');
    
    suggestions.innerHTML = '<h2><span class="icon icon-suggestion"></span>Suggestions</h2>' + 
        data.suggestions.map(suggestion => `
            <div class="suggestion">
                <p><strong>Suggestion:</strong> ${suggestion.suggestion}</p>
                <p><strong>Context:</strong> ${suggestion.context}</p>
            </div>
        `).join('');
}
