const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const activitySpan = document.getElementById('activity');
const scoreSpan = document.getElementById('score');
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const offBtn = document.getElementById('offBtn');

let stream;
let intervalId;
let selectedActivities = [];
let activityScores = {};

if (startBtn) startBtn.addEventListener('click', startRecognition);
if (stopBtn) stopBtn.addEventListener('click', stopRecognition);
if (offBtn) offBtn.addEventListener('click', offCamera);

// Athlete Fitness specific code
const selectActivitiesBtn = document.getElementById('selectActivities');
const activityForm = document.getElementById('activityForm');
const selectedActivitiesDiv = document.getElementById('selectedActivities');
const activityList = document.getElementById('activityList');
const avgScoreSpan = document.getElementById('avgScore');
const challengeForm = document.getElementById('challengeForm');
const challengesList = document.getElementById('challengesList');

// Gaming specific code
const selectGamingActivitiesBtn = document.getElementById('selectGamingActivities');
const gamingActivityForm = document.getElementById('gamingActivityForm');
const selectedGamingActivitiesDiv = document.getElementById('selectedGamingActivities');
const gamingActivityList = document.getElementById('gamingActivityList');
const gamingScoreSpan = document.getElementById('gamingScore');
const gamingChallengeForm = document.getElementById('gamingChallengeForm');
const gamingChallengesList = document.getElementById('gamingChallengesList');

if (selectActivitiesBtn) {
    selectActivitiesBtn.addEventListener('click', selectActivities);
}

if (challengeForm) {
    challengeForm.addEventListener('submit', addChallenge);
}

// Athlete Fitness specific buttons
const challengesBtn = document.getElementById('challengesBtn');
const performanceBtn = document.getElementById('performanceBtn');

if (challengesBtn) {
    challengesBtn.addEventListener('click', () => {
        window.location.href = '/challenges';
    });
}

if (performanceBtn) {
    performanceBtn.addEventListener('click', calculatePerformanceScore);
}

function calculatePerformanceScore() {
    // Calculate performance score based on selected activities
    const scores = Object.values(activityScores);
    const avg = scores.length > 0 ? scores.reduce((a, b) => a + b, 0) / scores.length : 0;
    alert(`Your current average performance score is: ${avg.toFixed(2)}`);
}

if (selectGamingActivitiesBtn) {
    selectGamingActivitiesBtn.addEventListener('click', selectGamingActivities);
}

if (gamingChallengeForm) {
    gamingChallengeForm.addEventListener('submit', addGamingChallenge);
}

function selectActivities() {
    const selectButtons = document.querySelectorAll('#activityForm .select-btn.selected');
    selectedActivities = Array.from(selectButtons).map(btn => btn.dataset.activity);
    if (selectedActivities.length > 0) {
        selectedActivitiesDiv.style.display = 'block';
        activityList.innerHTML = '';
        selectedActivities.forEach(activity => {
            const activityDiv = document.createElement('div');
            activityDiv.className = 'activity-item';
            activityDiv.innerHTML = `
                <h4>${activity.replace('_', ' ').toUpperCase()}</h4>
                <button class="btn on-camera-btn" data-activity="${activity}">On Camera</button>
                <button class="btn off-camera-btn" data-activity="${activity}">Off Camera</button>
                <span class="activity-score">Score: 0.00</span>
            `;
            activityList.appendChild(activityDiv);
            activityScores[activity] = 0;
        });
        updateAverageScore();
        // Add event listeners for camera buttons
        document.querySelectorAll('.on-camera-btn').forEach(btn => {
            btn.addEventListener('click', (e) => startActivityRecognition(e.target.dataset.activity));
        });
        document.querySelectorAll('.off-camera-btn').forEach(btn => {
            btn.addEventListener('click', (e) => stopActivityRecognition(e.target.dataset.activity));
        });
    } else {
        selectedActivitiesDiv.style.display = 'none';
    }
}

function startActivityRecognition(activity) {
    // Start web-based recognition for the selected activity
    startWebRecognition(activity);
    alert(`Recognition started for ${activity.replace('_', ' ')}.`);
}

function startWebRecognition(activity) {
    // Start web-based camera recognition for the specific activity
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function(stream) {
                const video = document.getElementById('video');
                const canvas = document.getElementById('canvas');
                const activitySpan = document.getElementById('activity');
                const scoreSpan = document.getElementById('score');

                if (video) {
                    video.srcObject = stream;
                    video.style.display = 'block';

                    // Start capturing frames
                    const intervalId = setInterval(() => {
                        if (video.videoWidth > 0) {
                            const context = canvas.getContext('2d');
                            canvas.width = video.videoWidth;
                            canvas.height = video.videoHeight;
                            context.drawImage(video, 0, 0, canvas.width, canvas.height);

                            const imageData = canvas.toDataURL('image/jpeg');

                            fetch('/predict', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                body: JSON.stringify({ image: imageData, selected_activities: [activity] }),
                            })
                            .then(response => response.json())
                            .then(data => {
                                if (activitySpan) activitySpan.textContent = data.activity;
                                if (scoreSpan) scoreSpan.textContent = data.score;

                                // Update activity score display
                                const activityItem = document.querySelector(`[data-activity="${activity}"]`);
                                if (activityItem) {
                                    const scoreElement = activityItem.parentElement.querySelector('.activity-score');
                                    if (scoreElement) {
                                        scoreElement.textContent = `Score: ${data.score}`;
                                    }
                                }
                            })
                            .catch(error => {
                                console.error('Error:', error);
                            });
                        }
                    }, 1000);

                    // Store interval ID for stopping later
                    video.dataset.intervalId = intervalId;
                }
            })
            .catch(function(err) {
                console.error('Error accessing camera:', err);
                alert('Error accessing camera. Please allow camera access.');
            });
    }
}

function stopActivityRecognition(activity) {
    // Stop recognition for the specific activity
    if (video && video.dataset.intervalId) {
        clearInterval(video.dataset.intervalId);
        video.dataset.intervalId = null;
    }
    if (video) {
        video.style.display = 'none';
    }
    if (activitySpan) activitySpan.textContent = 'Waiting...';
    if (scoreSpan) scoreSpan.textContent = '0.00';
    alert(`Recognition stopped for ${activity.replace('_', ' ')}.`);
}

function updateAverageScore() {
    const scores = Object.values(activityScores);
    const avg = scores.length > 0 ? scores.reduce((a, b) => a + b, 0) / scores.length : 0;
    if (avgScoreSpan) avgScoreSpan.textContent = avg.toFixed(2);
}

function addChallenge(e) {
    e.preventDefault();
    const desc = document.getElementById('challengeDesc').value;
    const date = document.getElementById('challengeDate').value;
    const time = document.getElementById('challengeTime').value;
    const challengeItem = document.createElement('div');
    challengeItem.className = 'challenge-item';
    challengeItem.innerHTML = `<p><strong>${desc}</strong> - ${date} at ${time}</p>`;
    challengesList.appendChild(challengeItem);
    challengeForm.reset();
}

function selectGamingActivities() {
    const checkboxes = document.querySelectorAll('#gamingActivityForm input[type="checkbox"]:checked');
    const selectedGamingActivities = Array.from(checkboxes).map(cb => cb.value);
    if (selectedGamingActivities.length > 0) {
        selectedGamingActivitiesDiv.style.display = 'block';
        gamingActivityList.innerHTML = '';
        selectedGamingActivities.forEach(activity => {
            const activityDiv = document.createElement('div');
            activityDiv.className = 'activity-item';
            activityDiv.innerHTML = `
                <h4>${activity.replace('_', ' ').toUpperCase()}</h4>
                <button class="btn on-camera-btn" data-activity="${activity}">On Camera</button>
                <button class="btn off-camera-btn" data-activity="${activity}">Off Camera</button>
                <span class="activity-score">Score: 0.00</span>
            `;
            gamingActivityList.appendChild(activityDiv);
        });
        // Add event listeners for camera buttons
        document.querySelectorAll('#gamingActivityList .on-camera-btn').forEach(btn => {
            btn.addEventListener('click', (e) => startGamingActivityRecognition(e.target.dataset.activity));
        });
        document.querySelectorAll('#gamingActivityList .off-camera-btn').forEach(btn => {
            btn.addEventListener('click', (e) => stopGamingActivityRecognition(e.target.dataset.activity));
        });
    } else {
        selectedGamingActivitiesDiv.style.display = 'none';
    }
}

function startGamingActivityRecognition(activity) {
    // Start main.py backend recognition for gaming
    fetch('/start_main_py', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        console.log('Main.py started for gaming:', data.message);
        alert(`Gaming recognition started for ${activity}. Check the backend console.`);
    })
    .catch(error => {
        console.error('Error starting main.py for gaming:', error);
    });
}

function stopGamingActivityRecognition(activity) {
    // Stop recognition (for now, just alert)
    alert(`Gaming recognition stopped for ${activity}.`);
}

function addGamingChallenge(e) {
    e.preventDefault();
    const desc = document.getElementById('gamingChallengeDesc').value;
    const date = document.getElementById('gamingChallengeDate').value;
    const time = document.getElementById('gamingChallengeTime').value;
    const challengeItem = document.createElement('div');
    challengeItem.className = 'challenge-item';
    challengeItem.innerHTML = `<p><strong>${desc}</strong> - ${date} at ${time}</p>`;
    gamingChallengesList.appendChild(challengeItem);
    gamingChallengeForm.reset();
}

async function startRecognition() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        startBtn.style.display = 'none';
        stopBtn.style.display = 'inline-block';
        offBtn.style.display = 'inline-block';

        // Start sending frames every second
        intervalId = setInterval(captureAndPredict, 1000);
    } catch (err) {
        console.error('Error accessing camera:', err);
        alert('Error accessing camera. Please allow camera access.');
    }
}

function stopRecognition() {
    if (intervalId) {
        clearInterval(intervalId);
        intervalId = null;
    }
    startBtn.style.display = 'inline-block';
    stopBtn.style.display = 'none';
    offBtn.style.display = 'inline-block';
    activitySpan.textContent = 'Waiting...';
    scoreSpan.textContent = '0.00';
}

function offCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }
    if (intervalId) {
        clearInterval(intervalId);
        intervalId = null;
    }
    video.srcObject = null;
    startBtn.style.display = 'inline-block';
    stopBtn.style.display = 'none';
    offBtn.style.display = 'none';
    activitySpan.textContent = 'Waiting...';
    scoreSpan.textContent = '0.00';
}

function captureAndPredict() {
    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    const imageData = canvas.toDataURL('image/jpeg');

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: imageData, selected_activities: selectedActivities }),
    })
    .then(response => response.json())
    .then(data => {
        activitySpan.textContent = data.activity;
        scoreSpan.textContent = data.score;
        // Update activity scores for average
        if (data.activity in activityScores) {
            activityScores[data.activity] = parseFloat(data.score);
            updateAverageScore();
            // Update individual activity score display
            const activityItem = document.querySelector(`[data-activity="${data.activity}"]`).parentElement;
            activityItem.querySelector('.activity-score').textContent = `Score: ${data.score}`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Activity selection logic
document.addEventListener('DOMContentLoaded', function() {
    const selectButtons = document.querySelectorAll('.select-btn');
    const selectedActivities = new Set();

    selectButtons.forEach(button => {
        button.addEventListener('click', function() {
            const activity = this.getAttribute('data-activity');
            if (selectedActivities.has(activity)) {
                selectedActivities.delete(activity);
                this.textContent = 'Select';
                this.style.background = '';
                this.classList.remove('selected');
            } else {
                selectedActivities.add(activity);
                this.textContent = 'Selected';
                this.style.background = 'linear-gradient(45deg, #28a745, #20c997)';
                this.classList.add('selected');
            }
        });
    });

    // Update global selected activities for camera functionality
    window.selectedActivities = selectedActivities;

    // Add event listeners for camera buttons
    const onCameraBtns = document.querySelectorAll('.on-camera-btn');
    const offCameraBtns = document.querySelectorAll('.off-camera-btn');

    onCameraBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const activity = this.getAttribute('data-activity');
            startActivityRecognition(activity);
        });
    });

    offCameraBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const activity = this.getAttribute('data-activity');
            stopActivityRecognition(activity);
        });
    });
});

// Stop recognition when page unloads
window.addEventListener('beforeunload', () => {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
    if (intervalId) {
        clearInterval(intervalId);
    }
});
