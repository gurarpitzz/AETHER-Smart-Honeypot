const tourSteps = [
    {
        element: null,
        title: "WELCOME COMMANDER",
        text: "This is AETHER. You are viewing a live cyber-defense operation. An AI is actively protecting the system from hackers. Let's show you how."
    },
    {
        element: "#metricsChart",
        title: "BATTLE PROGRESS",
        text: "The ORANGE line is our 'Confusion Index'. When it goes UP, it means the hacker is getting lost in our fake traps. We want this high!"
    },
    {
        element: "#threat-panel",
        title: "THE ENEMY",
        text: "Here we track the attacker details. We can see their fake IP and how 'Risky' their behavior is."
    },
    {
        element: "#defense-panel",
        title: "AETHER BRAIN",
        text: "The AI decides what Trap (Decoy) to deploy. Instead of blocking, it feeds them fake data to waste their time."
    },
    {
        element: "#log-terminal",
        title: "LIVE FEED",
        text: "Every single move - attacked and defended - is logged here in real-time. Watch the battle unfold."
    }
];

let currentStep = 0;

function startTour() {
    currentStep = 0;
    createOverlay();
    showStep(currentStep);
}

function createOverlay() {
    const overlay = document.createElement('div');
    overlay.id = 'tour-overlay';
    document.body.appendChild(overlay);

    const box = document.createElement('div');
    box.id = 'tour-box';
    box.innerHTML = `
        <h2 id="tour-title">Title</h2>
        <p id="tour-text">Text</p>
        <button onclick="nextStep()">NEXT ></button>
        <button onclick="endTour()" style="float:left; border-color:#553300; color:#553300">SKIP</button>
    `;
    document.body.appendChild(box);
}

function showStep(index) {
    if (index >= tourSteps.length) {
        endTour();
        return;
    }

    document.querySelectorAll('.tour-highlight').forEach(el => {
        el.classList.remove('tour-highlight');
    });

    const step = tourSteps[index];
    const box = document.getElementById('tour-box');

    const titleEl = document.getElementById('tour-title');
    const textEl = document.getElementById('tour-text');

    titleEl.innerText = step.title;
    textEl.innerText = step.text;

    // Reset center transform
    box.style.transform = "none";

    // Determine target element
    let target = null;
    if (step.element) target = document.querySelector(step.element);

    if (!target) {
        // Center welcome step
        box.style.top = "35%";
        box.style.left = "50%";
        box.style.transform = "translate(-50%, -50%)";
        return;
    }

    // Highlight
    target.classList.add('tour-highlight');
    target.scrollIntoView({ behavior: "smooth", block: "center" });

    const rect = target.getBoundingClientRect();

    let top = rect.bottom + 20;
    let left = rect.left + rect.width / 2 - 150;

    // Flip above target if not enough space
    if (top + 250 > window.innerHeight) {
        top = rect.top - 220;
    }

    // ---- CLAMP FIX — NEVER GO OUTSIDE SCREEN ----
    const boxWidth = 320;   // approx
    const boxHeight = 220;  // approx

    // Clamp vertical
    if (top < 10) top = 10;
    if (top + boxHeight > window.innerHeight - 10) {
        top = window.innerHeight - boxHeight - 10;
    }

    // Clamp horizontal
    if (left < 10) left = 10;
    if (left + boxWidth > window.innerWidth - 10) {
        left = window.innerWidth - boxWidth - 10;
    }
    // ------------------------------------------------

    box.style.top = top + "px";
    box.style.left = left + "px";
}

function nextStep() {
    currentStep++;
    showStep(currentStep);
}

function endTour() {
    const overlay = document.getElementById('tour-overlay');
    const box = document.getElementById('tour-box');
    if (overlay) overlay.remove();
    if (box) box.remove();

    document.querySelectorAll('.tour-highlight').forEach(el => {
        el.classList.remove('tour-highlight');
    });
}
