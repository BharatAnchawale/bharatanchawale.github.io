const uploadForm = document.getElementById("uploadForm");
const videoInput = document.getElementById("videoInput");
const statusDiv = document.getElementById("status");
const downloadSection = document.getElementById("downloadSection");
const downloadLink = document.getElementById("downloadLink");

// Set backend URL
const API_BASE = "http://localhost:8000";

uploadForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const file = videoInput.files[0];
    if (!file) return;

    statusDiv.textContent = "";
    document.getElementById("logWindow").textContent = ""; // Clear log
    downloadSection.style.display = "none";

    const formData = new FormData();
    formData.append("file", file);

    // Show progress UI
    document.getElementById("progressContainer").style.display = "block";
    updateProgress(0);

    try {
        const response = await fetchWithFakeProgress(`${API_BASE}/upload/`, formData);

        const result = await response.json();
        const videoId = result.video_id;

        updateProgress(100);

        logMessage("Your encrypted video is ready to download.");


        setTimeout(() => {
            document.getElementById("progressStatus").textContent = "Done!";
            downloadLink.href = `${API_BASE}/download/${videoId}`;
            downloadLink.textContent = `Download Encrypted Video (${videoId})`;
            downloadSection.style.display = "block";
        }, 500);
    } catch (err) {
        console.error(err);
        statusDiv.textContent = `Error: ${err.message}`;
        document.getElementById("progressStatus").textContent = "Failed";
    }
});

function updateProgress(percent) {
    const fill = document.getElementById("progressFill");
    const status = document.getElementById("progressStatus");

    fill.style.width = `${percent}%`;

    if (percent <= 20) status.textContent = "Uploading...";
    else if (percent <= 40) status.textContent = "Encrypting...";
    else if (percent <= 60) status.textContent = "Storing...";
    else if (percent <= 80) status.textContent = "Converting...";
    else status.textContent = "Finalizing...";
}

// Simulate progress manually since we can't track real backend progress
async function fetchWithFakeProgress(url, formData) {
    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open("POST", url);

        xhr.onload = () => {
            if (xhr.status >= 200 && xhr.status < 300) {
                resolve(new Response(xhr.responseText, {
                    status: xhr.status,
                    headers: { "Content-Type": "application/json" }
                }));
            } else {
                reject(new Error(xhr.statusText));
            }
        };

        xhr.onerror = () => reject(new Error("Network Error"));

        // Fake progress steps
        let percent = 0;
        const interval = setInterval(() => {
            percent += 10;
            updateProgress(percent);

            if (percent === 10) logMessage("Uploading your video...");
            else if (percent === 30) logMessage("Encrypting securely...");
            else if (percent === 50) logMessage("Storing in secure cloud...");
            else if (percent === 70) logMessage("Converting video format...");
            else if (percent === 90) logMessage("Almost ready for download...");

            if (percent >= 90) clearInterval(interval);
        }, 300);


        xhr.send(formData);
    });
}

function logMessage(message, type = "info") {
  const logWindow = document.getElementById("logWindow");
  const now = new Date();
  const timestamp = now.toLocaleTimeString();
  const label = type === "error" ? "[ERROR]" : "[INFO]";
  const logEntry = `[${timestamp}] ${label} ${message}`;

  logWindow.innerHTML += ` ${logEntry}\n`;
  logWindow.scrollTop = logWindow.scrollHeight;
}

function toggleLog() {
  const logWindow = document.getElementById("logWindow");
  const toggleBtn = document.getElementById("toggleLogBtn");

  if (logWindow.style.display === "none") {
    logWindow.style.display = "block";
    toggleBtn.innerText = "Hide Log";
  } else {
    logWindow.style.display = "none";
    toggleBtn.innerText = "Show Log";
  }
}


