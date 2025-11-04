// Performance page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Load performance data from sessionStorage
    const performanceData = JSON.parse(sessionStorage.getItem('performanceData'));

    if (performanceData) {
        // Display overall score
        const overallScoreElement = document.getElementById('overallScore');
        if (overallScoreElement) {
            overallScoreElement.textContent = performanceData.overall_score;
        }

        // Display activity breakdown
        const activityScoresElement = document.getElementById('activityScores');
        if (activityScoresElement && performanceData.activity_scores) {
            activityScoresElement.innerHTML = '';
            Object.entries(performanceData.activity_scores).forEach(([activity, score]) => {
                const activityDiv = document.createElement('div');
                activityDiv.className = 'activity-score-item';
                activityDiv.innerHTML = `
                    <span class="activity-name">${activity.replace('_', ' ').toUpperCase()}</span>
                    <span class="activity-score">${score.toFixed(2)}</span>
                `;
                activityScoresElement.appendChild(activityDiv);
            });
        }

        // Display insights
        const insightsElement = document.getElementById('insights');
        if (insightsElement && performanceData.insights) {
            insightsElement.innerHTML = '';
            performanceData.insights.forEach(insight => {
                const insightDiv = document.createElement('div');
                insightDiv.className = 'insight-item';
                insightDiv.textContent = insight;
                insightsElement.appendChild(insightDiv);
            });
        }
    }

    // Back to fitness button
    const backBtn = document.getElementById('backToFitness');
    if (backBtn) {
        backBtn.addEventListener('click', function() {
            window.location.href = '/athlete_fitness';
        });
    }

    // Save score button (placeholder functionality)
    const saveBtn = document.getElementById('saveScore');
    if (saveBtn) {
        saveBtn.addEventListener('click', function() {
            alert('Score saved successfully!');
            // Here you could implement actual saving to database
        });
    }
});
