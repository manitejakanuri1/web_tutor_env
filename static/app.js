const API_BASE = window.location.origin;

let currentState = null;
let demoActive = false;

async function sleep(ms) {
    return new Promise(r => setTimeout(r, ms));
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
    currentState = envelope.state;

    // Headings
    document.getElementById('task-title').innerText = obs.title;
    document.getElementById('instruction-text').innerText = obs.instruction;
    document.getElementById('difficulty-badge').innerText = obs.difficulty;
    
    // Status metrics
    document.getElementById('phase-display').innerText = obs.phase;
    document.getElementById('score-display').innerText = envelope.reward.toFixed(2);
    
    // Energy Bar
    const budget = currentState.energy_budget;
    const current = obs.energy_remaining !== undefined ? obs.energy_remaining : obs.energy;
    document.getElementById('energy-text').innerText = `${current}/${budget}`;
    const pct = budget > 0 ? (current / budget) * 100 : 0;
    document.getElementById('energy-fill').style.width = `${pct}%`;
    document.getElementById('energy-fill').style.background = pct < 30 ? 'var(--danger)' : 'var(--warning)';

    // Dynamic Actions
    renderActions(obs.available_actions);

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
        if (actStr === 'restart_task') return; // Handled by standard reset
        
        const btn = document.createElement('button');
        btn.className = 'btn';
        
        let label = actStr;
        let actionPayload = null;
        
        if (actStr === 'read_section') return; // Handled visually
        if (actStr === 'select_answer' || actStr === 'toggle_answer') return; // Handled in quiz DOM
        if (actStr === 'submit_quiz') return; // Handled by big submit button
        
        if (actStr === 'navigate(quiz)') {
            label = "Go to Quiz »";
            actionPayload = { action_type: "navigate", target: "quiz" };
        } else if (actStr === 'navigate(study)') {
            label = "« Back to Study";
            actionPayload = { action_type: "navigate", target: "study" };
        } else if (actStr === 'use_hint') {
            label = "Use Hint (-2 Energy)";
            // We'll hardcode requesting hint for q1 if not specified, 
            // but usually hint is per question. For simplicity, we trigger first unanswered.
            actionPayload = { action_type: "use_hint", question_id: "q1" }; 
        } else if (actStr === 'retry_quiz') {
            label = "Retry Quiz";
            actionPayload = { action_type: "retry_quiz" };
        }

        btn.innerText = label;
        if (actionPayload) {
            btn.onclick = () => doAction(actionPayload);
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
    
    obs.sections.forEach(sec => {
        const li = document.createElement('li');
        li.className = `section-item ${sec.read ? 'read' : ''}`;
        li.innerText = sec.title;
        li.onclick = () => {
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

    obs.questions.forEach(q => {
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
    document.getElementById('final-score').innerText = (state.score * 100).toFixed(0) + '%';
    document.getElementById('review-feedback').innerText = state.last_feedback;

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
    setTimeout(() => { toast.classList.add('hidden'); }, 3000);
}

async function doAction(payload) {
    const res = await apiCall('/step', payload);
    renderState(res);
}

document.getElementById('btn-reset').onclick = async () => {
    demoActive = false;
    if(document.getElementById('btn-demo')) {
        document.getElementById('btn-demo').innerText = "🤖 Watch AI Play";
    }
    const selector = document.getElementById('task-selector');
    const val = selector ? selector.value : 'random';
    const payload = val === 'random' ? {} : { task_index: parseInt(val) };
    const res = await apiCall('/reset', payload); 
    renderState(res);
};
document.getElementById('btn-submit-quiz').onclick = () => {
    demoActive = false; // user took control
    doAction({ action_type: "submit_quiz" });
};

// Agent Demo Logic
if(document.getElementById('btn-demo')) {
    document.getElementById('btn-demo').onclick = async () => {
        if (demoActive) {
            demoActive = false;
            document.getElementById('btn-demo').innerText = "🤖 Watch AI Play";
            showFeedback("Demo mode stopped.");
            return;
        }
        
        demoActive = true;
        document.getElementById('btn-demo').innerText = "🛑 Stop Demo";
        showFeedback("AI Agent taking over...");
        
        while(demoActive) {
            await sleep(800); // Artificial delay to simulate thinking/reading
            if (!demoActive) break;
            
            let obs = null;
            try {
                const stateRes = await apiCall('/state');
                if(stateRes && stateRes.observation) obs = stateRes.observation;
            } catch(e) {}
            
            if (!obs) break;
            if (obs.phase === 'completed') {
                demoActive = false;
                document.getElementById('btn-demo').innerText = "🤖 Watch AI Play";
                showFeedback("Agent interaction complete!");
                break;
            }
            
            const actions = obs.available_actions;
            if (!actions || actions.length === 0) break;
            
            let pickedPayload = null;
            
            if (obs.phase === 'study') {
                const unread = obs.sections.find(s => !s.read);
                if (unread) {
                    pickedPayload = { action_type: "read_section", section_id: unread.section_id };
                } else if (actions.includes('navigate(quiz)')) {
                    pickedPayload = { action_type: "navigate", target: "quiz" };
                }
            } 
            else if (obs.phase === 'quiz') {
                let unanswered = obs.questions.find(q => !q.your_answer || q.your_answer.length === 0);
                if (unanswered) {
                    const actType = unanswered.type === 'multi' ? 'toggle_answer' : 'select_answer';
                    pickedPayload = { action_type: actType, question_id: unanswered.question_id, option_index: 0 }; // AI randomly picks option 0 just for demo
                } else if (actions.includes('submit_quiz')) {
                    pickedPayload = { action_type: "submit_quiz" };
                }
            }
            
            if (pickedPayload) {
                await doAction(pickedPayload);
            } else {
                demoActive = false;
                document.getElementById('btn-demo').innerText = "🤖 Watch AI Play";
                break;
            }
        }
    };
}

// Auto start
window.onload = async () => {
    const stateRes = await apiCall('/state');
    if (!stateRes || !stateRes.observation || !stateRes.observation.available_actions) {
        document.getElementById('btn-reset').click();
    } else {
        renderState(stateRes);
    }
};
