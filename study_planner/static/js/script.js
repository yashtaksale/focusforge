// 1. AI Typewriter Effect (Refined for Your AI Architect Aesthetic)
const subTitle = document.querySelector('.text-secondary');
const introText = "Leveling up your Academic Architecture..."; 
let charIndex = 0;

function typeWriter() {
    if (charIndex < introText.length) {
        subTitle.innerHTML = introText.slice(0, charIndex + 1) + '<span class="animate-pulse">|</span>';
        charIndex++;
        setTimeout(typeWriter, 50);
    }
}

// 2. Requirement: Auto-Generate Timetable & Daily Task Checklist
function generateSmartTimetable(subject) {
    const listContainer = document.getElementById('missionList'); 
    
    const sessions = [
        { name: `${subject}: Logic & Flowchart`, icon: 'fa-project-diagram' },
        { name: `${subject}: Implementation Lab`, icon: 'fa-laptop-code' },
        { name: `${subject}: Security Audit / Forensics`, icon: 'fa-user-shield' }
    ];

    sessions.forEach(session => {
        const li = document.createElement('li');
        li.className = "list-group-item bg-transparent text-white d-flex justify-content-between align-items-center mb-3 border rounded border-secondary hover-glow animate__animated animate__zoomIn";
        
        // Dynamic Icon Logic for Java and Forensics
        let subjectIcon = `<i class="fas ${session.icon} text-info me-3"></i>`;
        if (subject.toLowerCase().includes('java')) subjectIcon = '<i class="fab fa-java text-warning me-3"></i>';
        if (subject.toLowerCase().includes('forensics')) subjectIcon = '<i class="fas fa-search-plus text-info me-3"></i>';

        li.innerHTML = `
            <div class="d-flex align-items-center">
                <input type="checkbox" class="task-checkbox mission-checkbox me-3" onchange="updateSystemProgress()">
                <span class="mission-name">${subjectIcon} ${session.name}</span>
            </div>
            <span class="badge rounded-pill bg-dark border border-info text-info">READY</span>
        `;
        listContainer.appendChild(li);
    });
    updateSystemProgress();
}

// 3. Requirement: Progress Tracker Bar Logic
function updateSystemProgress() {
    const totalTasks = document.querySelectorAll('.mission-checkbox').length;
    const completedTasks = document.querySelectorAll('.mission-checkbox:checked').length;
    const progressFill = document.getElementById('mainProgressBar');
    
    const percentage = totalTasks === 0 ? 0 : Math.round((completedTasks / totalTasks) * 100);
    
    progressFill.style.width = percentage + '%';
    progressFill.innerHTML = `${percentage}% MISSION SYNCED`;
    
    if (percentage === 100 && totalTasks > 0) {
        progressFill.classList.replace('bg-info', 'bg-success');
        progressFill.style.boxShadow = "0 0 25px #198754";
        showCelebration();
    } else {
        progressFill.classList.replace('bg-success', 'bg-info');
        progressFill.style.boxShadow = "0 0 15px rgba(0, 212, 255, 0.4)";
    }
}

// Extra: Console Celebration
function showCelebration() {
    console.log("%c MISSION ACCOMPLISHED! SYSTEM OPTIMAL ", "background: #198754; color: white; font-size: 20px; font-weight: bold;");
}

// 4. Requirement: Download Timetable Option
function downloadPlan() {
    const tasks = document.querySelectorAll('.mission-name');
    if (tasks.length === 0) return alert("System Error: No active missions found to export.");

    let content = "--- SAHAYAK AI STUDY PLAN ---\n";
    content += "Generated: " + new Date().toLocaleString() + "\n\n";
    
    tasks.forEach((t, i) => {
        content += `[ MISSION ${i + 1} ]: ${t.innerText}\n`;
    });

    const element = document.createElement('a');
    const file = new Blob([content], {type: 'text/plain'});
    element.href = URL.createObjectURL(file);
    element.download = "My_Study_Plan.txt";
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

// 5. Form & Event Handling
const missionForm = document.getElementById('missionForm');
if (missionForm) {
    missionForm.addEventListener('submit', function(e) {
        e.preventDefault(); 
        const subjectInput = document.querySelector('input[name="subject"]');
        if (subjectInput.value.trim() !== "") {
            generateSmartTimetable(subjectInput.value);
            subjectInput.value = ""; 
        }
    });
}

window.onload = () => {
    typeWriter();
    updateSystemProgress();
};