const API_BASE = window.location.origin;

let currentState = null;
let demoActive = false;
let lastObservation = null;

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function apiCall(endpoint, payload = null) {
    const options = {
        method: payload ? 'POST' : 'GET',
        headers: { 'Content-Type': 'application/json' },
    };
    if (payload) options.body = JSON.stringify(payload);

    try {
        const res = await fetch(`${API_BASE}${endpoint}`, options);
        return await res.json();
    } catch (e) {
        console.error("API Error", e);
        showFeedback("Error connecting to server.");
        return null;
    }
}

async function renderState(envelope) {
    if (!envelope) return;
    const obs = envelope.observation;
    if (!obs) return;
    currentState = envelope.state;
    lastObservation = obs;

    // Headings
    document.getElementById('task-title').innerText = obs.title || '';
    document.getElementById('instruction-text').innerText = obs.instruction || '';
    document.getElementById('difficulty-badge').innerText = obs.difficulty || '';

    // Status metrics
    document.getElementById('phase-display').innerText = obs.phase || '';
    const scoreVal = currentState.quiz_score !== undefined ? currentState.quiz_score : 0;
    const rewardVal = currentState.score !== undefined ? currentState.score : 0;
    document.getElementById('score-display').innerText = (scoreVal * 100).toFixed(0) + '% (R:' + rewardVal.toFixed(2) + ')';

    // Energy Bar
    const budget = currentState.energy_budget || 0;
    const current = obs.energy_remaining !== undefined ? obs.energy_remaining : (obs.energy || 0);
    document.getElementById('energy-text').innerText = `${current}/${budget}`;
    const pct = budget > 0 ? (current / budget) * 100 : 0;
    document.getElementById('energy-fill').style.width = `${pct}%`;
    document.getElementById('energy-fill').style.background = pct < 30 ? 'var(--danger)' : 'var(--warning)';

    // Dynamic Actions
    renderActions(obs.available_actions || []);

    // Feedback Toast
    if (obs.last_feedback) {
        showFeedback(obs.last_feedback);
    }

    // View Switching
    hideAllViews();
    if (obs.phase === 'study') {
        document.getElementById('view-study').classList.remove('hidden');
        renderStudyPhase(obs);
    } else if (obs.phase === 'quiz') {
        document.getElementById('view-quiz').classList.remove('hidden');
        renderQuizPhase(obs);
    } else {
        document.getElementById('view-review').classList.remove('hidden');
        renderReviewPhase(obs, currentState);
    }
}

function hideAllViews() {
    document.getElementById('view-study').classList.add('hidden');
    document.getElementById('view-quiz').classList.add('hidden');
    document.getElementById('view-review').classList.add('hidden');
}

function renderActions(actions) {
    const container = document.getElementById('dynamic-actions');
    container.innerHTML = '';

    actions.forEach(actStr => {
        if (actStr === 'restart_task') return;

        const btn = document.createElement('button');
        btn.className = 'btn';

        let label = actStr;
        let actionPayload = null;

        if (actStr === 'read_section') return;
        if (actStr === 'select_answer' || actStr === 'toggle_answer') return;
        if (actStr === 'submit_quiz') return;

        if (actStr === 'navigate(quiz)') {
            label = "Go to Quiz »";
            actionPayload = { action_type: "navigate", target: "quiz" };
        } else if (actStr === 'navigate(study)') {
            label = "« Back to Study";
            actionPayload = { action_type: "navigate", target: "study" };
        } else if (actStr === 'use_hint') {
            label = "Use Hint (-2 Energy)";
            actionPayload = { action_type: "use_hint", question_id: "q1" };
        } else if (actStr === 'retry_quiz') {
            label = "Retry Quiz";
            actionPayload = { action_type: "retry_quiz" };
        }

        btn.innerText = label;
        if (actionPayload) {
            btn.onclick = () => {
                demoActive = false; // user took manual control
                doAction(actionPayload);
            };
            container.appendChild(btn);
        }
    });

    if (actions.includes('submit_quiz')) {
        document.getElementById('btn-submit-quiz').classList.remove('hidden');
    } else {
        document.getElementById('btn-submit-quiz').classList.add('hidden');
    }
}

function renderStudyPhase(obs) {
    const ul = document.getElementById('materials-ul');
    ul.innerHTML = '';

    (obs.sections || []).forEach(sec => {
        const li = document.createElement('li');
        li.className = `section-item ${sec.read ? 'read' : ''}`;
        li.innerText = sec.title;
        li.onclick = () => {
            demoActive = false; // user took manual control
            doAction({ action_type: "read_section", section_id: sec.section_id });
        };
        ul.appendChild(li);
    });

    if (obs.current_content) {
        document.getElementById('reading-content').innerText = obs.current_content;
    } else {
        document.getElementById('reading-content').innerHTML = "<em>Select a module to begin reading...</em>";
    }
}

function renderQuizPhase(obs) {
    const container = document.getElementById('questions-container');
    container.innerHTML = '';

    (obs.questions || []).forEach(q => {
        const card = document.createElement('div');
        card.className = 'question-card';

        const typeHint = q.type === 'multi' ? ' (Select ALL that apply)' : '';
        card.innerHTML = `<h3>${q.question}${typeHint}</h3>`;

        const optsList = document.createElement('div');
        optsList.className = 'options-list';

        const currentAnswers = q.your_answer || [];

        q.options.forEach((optStr, idx) => {
            const optBox = document.createElement('div');
            const isSelected = currentAnswers.includes(idx);
            optBox.className = `option-box ${isSelected ? 'selected' : ''}`;
            optBox.innerText = optStr;

            optBox.onclick = () => {
                demoActive = false; // user took manual control
                const actType = q.type === 'multi' ? 'toggle_answer' : 'select_answer';
                doAction({ action_type: actType, question_id: q.question_id, option_index: idx });
            };
            optsList.appendChild(optBox);
        });

        card.appendChild(optsList);
        container.appendChild(card);
    });
}

function renderReviewPhase(obs, state) {
    // Show quiz accuracy in the big circle, NOT the RL reward
    const quizPct = (state.quiz_score !== undefined ? state.quiz_score : 0);
    const rewardVal = (state.score !== undefined ? state.score : 0);
    document.getElementById('final-score').innerText = (quizPct * 100).toFixed(0) + '%';
    document.getElementById('review-feedback').innerText =
        (state.last_feedback || 'Episode finished.') +
        '\nRL Reward: ' + rewardVal.toFixed(2) + ' | Quiz Accuracy: ' + (quizPct * 100).toFixed(0) + '%';

    const container = document.getElementById('review-questions');
    container.innerHTML = '';

    if (state.quiz_results) {
        state.quiz_results.forEach(res => {
            const div = document.createElement('div');
            div.className = `review-item ${res.correct ? 'correct' : 'wrong'}`;
            div.innerHTML = `
                <strong>${res.question_id}</strong>:
                Partial Score: ${res.partial_score} <br/>
                <em>${res.feedback}</em>
            `;
            container.appendChild(div);
        });
    }
}

function showFeedback(msg) {
    const toast = document.getElementById('feedback-toast');
    toast.innerText = msg;
    toast.classList.remove('hidden');
    setTimeout(() => { toast.classList.add('hidden'); }, 3500);
}

async function doAction(payload) {
    const res = await apiCall('/step', payload);
    await renderState(res);
    return res;
}

async function resetEpisode() {
    const selector = document.getElementById('task-selector');
    const val = selector ? selector.value : 'random';
    const payload = val === 'random' ? {} : { task_index: parseInt(val) };
    const res = await apiCall('/reset', payload);
    await renderState(res);
    return res;
}

// ============================================================
//  AGENT DEMO MODE — fully self-contained
// ============================================================
async function startAgentDemo() {
    const btnDemo = document.getElementById('btn-demo');

    // If already running, stop it
    if (demoActive) {
        demoActive = false;
        btnDemo.innerText = "🤖 Watch AI Play";
        showFeedback("Demo stopped.");
        return;
    }

    demoActive = true;
    btnDemo.innerText = "🛑 Stop Demo";
    showFeedback("🤖 AI Agent initializing...");

    // Step 0 — always reset to a fresh episode so the demo has a clean slate
    await resetEpisode();
    await sleep(600);

    // Main demo loop
    let safety = 0;
    const MAX_STEPS = 50; // guard against infinite loops

    while (demoActive && safety < MAX_STEPS) {
        safety++;
        if (!demoActive) break;

        // Re-read the latest observation from the last renderState call
        const obs = lastObservation;
        if (!obs) {
            showFeedback("Lost connection to environment.");
            break;
        }

        const phase = obs.phase;
        const actions = obs.available_actions || [];

        // ---- COMPLETED ----
        if (phase === 'completed' || phase === 'review') {
            demoActive = false;
            btnDemo.innerText = "🤖 Watch AI Play";
            showFeedback("✅ Agent finished the episode!");
            break;
        }

        let pickedPayload = null;

        // ---- STUDY PHASE ----
        if (phase === 'study') {
            // Read unread sections one by one
            const unread = (obs.sections || []).find(s => !s.read);
            if (unread) {
                showFeedback(`📖 Reading: ${unread.title}`);
                pickedPayload = { action_type: "read_section", section_id: unread.section_id };
            } else if (actions.includes('navigate(quiz)')) {
                showFeedback("📝 All sections read — moving to Quiz...");
                pickedPayload = { action_type: "navigate", target: "quiz" };
            }
        }

        // ---- QUIZ PHASE ----
        else if (phase === 'quiz') {
            const questions = obs.questions || [];
            // Find a question that hasn't been answered yet
            let unanswered = questions.find(q => !q.your_answer || q.your_answer.length === 0);
            if (unanswered) {
                // Pick a random option to look more "intelligent"
                const numOptions = unanswered.options ? unanswered.options.length : 1;
                const pick = Math.floor(Math.random() * numOptions);
                const actType = unanswered.type === 'multi' ? 'toggle_answer' : 'select_answer';
                showFeedback(`🤔 Answering: ${unanswered.question_id} → option ${pick + 1}`);
                pickedPayload = { action_type: actType, question_id: unanswered.question_id, option_index: pick };
            } else if (actions.includes('submit_quiz')) {
                showFeedback("📊 Submitting quiz...");
                pickedPayload = { action_type: "submit_quiz" };
            }
        }

        // Execute the picked action
        if (pickedPayload && demoActive) {
            await sleep(900); // pause so user can see what's happening
            if (!demoActive) break;
            await doAction(pickedPayload);
            await sleep(400); // brief pause after UI updates
        } else {
            // No valid action found — stop
            demoActive = false;
            btnDemo.innerText = "🤖 Watch AI Play";
            showFeedback("Agent has no more actions available.");
            break;
        }
    }

    // Cleanup
    demoActive = false;
    btnDemo.innerText = "🤖 Watch AI Play";
}

// ============================================================
//  WIRE UP ALL EVENTS — inside DOMContentLoaded so DOM is ready
// ============================================================
document.addEventListener('DOMContentLoaded', async () => {

    // Reset button
    document.getElementById('btn-reset').addEventListener('click', async () => {
        demoActive = false;
        document.getElementById('btn-demo').innerText = "🤖 Watch AI Play";
        await resetEpisode();
    });

    // Submit quiz button
    document.getElementById('btn-submit-quiz').addEventListener('click', () => {
        demoActive = false;
        doAction({ action_type: "submit_quiz" });
    });

    // **Watch AI Play** button
    document.getElementById('btn-demo').addEventListener('click', () => {
        startAgentDemo();
    });

    // Auto-start: load existing state or reset
    const stateRes = await apiCall('/state');
    if (!stateRes || !stateRes.observation || !stateRes.observation.available_actions) {
        await resetEpisode();
    } else {
        await renderState(stateRes);
    }
});
