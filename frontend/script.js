// ==========================================
// AI Sign Language Translator
// Frontend V2
// ==========================================

// Backend URL
const BACKEND_URL = "http://127.0.0.1:5000";

// Elements
const video = document.getElementById("video");

const startBtn = document.getElementById("start-btn");
const stopBtn = document.getElementById("stop-btn");
const speakBtn = document.getElementById("speak-btn");
const clearBtn = document.getElementById("clear-btn");

const gesture = document.getElementById("gesture");
const translation = document.getElementById("translation");

const confidence = document.getElementById("confidence");
const confidenceBar = document.getElementById("confidence-bar");

const status = document.getElementById("status");

const language = document.getElementById("language");

const themeToggle = document.getElementById("theme-toggle");

let cameraRunning = false;

// ==========================================
// Start Camera
// ==========================================

function startCamera() {

    if(cameraRunning) return;

    video.src = BACKEND_URL + "/video";

    status.innerHTML = "Camera Running";
    status.className = "badge bg-success";

    cameraRunning = true;

}

// ==========================================
// Stop Camera
// ==========================================

function stopCamera(){

    video.src = "";

    status.innerHTML = "Camera Stopped";
    status.className = "badge bg-danger";

    cameraRunning = false;

}

// ==========================================
// Clear Results
// ==========================================

async function clearResults() {

    try {

        await fetch(BACKEND_URL + "/clear");

        gesture.innerHTML = "--";

        translation.innerHTML = "";

        confidence.innerHTML = "0%";

        confidenceBar.style.width = "0%";

    } catch (error) {

        console.log(error);

    }

}

// ==========================================
// Speak Translation
// ==========================================

function speakTranslation() {

    const text = translation.innerHTML.trim();

    if (text === "") {
        alert("No sentence available to speak.");
        return;
    }

    window.speechSynthesis.cancel();

    const speech = new SpeechSynthesisUtterance(text);

    const selectedLanguage =
        document.getElementById("language").value;

    speech.lang = selectedLanguage;

    speech.rate = 1;

    speech.pitch = 1;

    speech.volume = 1;

    window.speechSynthesis.speak(speech);

}

// ==========================================
// Theme Toggle
// ==========================================

themeToggle.onclick = ()=>{

    document.body.classList.toggle("dark");

}

// ==========================================
// Demo Data (Temporary)
// Replace later with Flask API
// ==========================================

function updatePrediction(text, percent){

    gesture.innerHTML = text;

    translation.innerHTML = text;

    confidence.innerHTML = percent + "%";

    confidenceBar.style.width = percent + "%";

}

async function getPrediction() {

    if (!cameraRunning) return;

    try {

        const response = await fetch(BACKEND_URL + "/prediction");

        const data = await response.json();

        // Current gesture
        gesture.innerHTML = data.gesture;

        // Complete translated sentence
        translation.innerHTML = data.sentence || "";

        // Confidence
        confidence.innerHTML = data.confidence.toFixed(2) + "%";

        confidenceBar.style.width = data.confidence + "%";

    } catch (error) {

        console.log(error);

    }

}

setInterval(getPrediction, 500);

// ==========================================
// Events
// ==========================================

startBtn.onclick=startCamera;

stopBtn.onclick=stopCamera;

clearBtn.onclick=clearResults;

speakBtn.onclick=speakTranslation;