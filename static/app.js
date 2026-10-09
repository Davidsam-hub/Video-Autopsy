const videoInput = document.getElementById("videoInput");
const uploadBox = document.getElementById("uploadBox");
const uploadButton = document.getElementById("uploadButton");
const fileName = document.getElementById("fileName");
const status = document.getElementById("status");

const videoPreview = document.getElementById("videoPreview");
const results = document.getElementById("results");

const summary = document.getElementById("summary");
const keyPoints = document.getElementById("keyPoints");
const sentiment = document.getElementById("sentiment");
const sentimentExplanation = document.getElementById("sentimentExplanation");
const topics = document.getElementById("topics");
const actions = document.getElementById("actions");
const transcript = document.getElementById("transcript");

const copyTranscript = document.getElementById("copyTranscript");
const newAnalysisButton = document.getElementById("newAnalysisButton");
const downloadAnalysis = document.getElementById("downloadAnalysis");

let previewUrl = null;


/* =========================
   FILE HANDLING
========================= */

function handleVideo(file) {

    if (!file) {
        resetFile();
        return;
    }

    if (!file.type.startsWith("video/")) {
        showError("Please select a valid video file.");
        videoInput.value = "";
        return;
    }

    if (file.size > 500 * 1024 * 1024) {
        showError("Video must be smaller than 500MB.");
        videoInput.value = "";
        return;
    }

    fileName.textContent = `Selected: ${file.name}`;

    if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
    }

    previewUrl = URL.createObjectURL(file);

    videoPreview.src = previewUrl;
    videoPreview.style.display = "block";

    uploadButton.disabled = false;

    status.textContent = "";
}


function resetFile() {

    fileName.textContent = "No video selected";

    videoPreview.pause();
    videoPreview.removeAttribute("src");
    videoPreview.load();

    videoPreview.style.display = "none";

    uploadButton.disabled = true;
}


/* =========================
   FILE INPUT
========================= */

videoInput.addEventListener("change", () => {

    const file = videoInput.files[0];

    handleVideo(file);

});


/* =========================
   DRAG & DROP
========================= */

uploadBox.addEventListener("dragover", (event) => {

    event.preventDefault();

    uploadBox.classList.add("dragging");

});


uploadBox.addEventListener("dragleave", () => {

    uploadBox.classList.remove("dragging");

});


uploadBox.addEventListener("drop", (event) => {

    event.preventDefault();

    uploadBox.classList.remove("dragging");

    const file = event.dataTransfer.files[0];

    if (!file) {
        return;
    }

    videoInput.files = event.dataTransfer.files;

    handleVideo(file);

});


/* =========================
   STATUS HELPERS
========================= */

function setStatus(message) {

    status.textContent = message;

}


function showError(message) {

    setStatus(`❌ ${message}`);

}


function showLoading() {

    uploadButton.disabled = true;

    uploadButton.textContent = "Analyzing...";

    setStatus("⏳ Extracting audio...");
}


/* =========================
   DISPLAY ANALYSIS
========================= */

function displayAnalysis(analysis) {

    summary.textContent =
        analysis.summary || "No summary available.";


    /* KEY POINTS */

    keyPoints.innerHTML = "";

    if (analysis.key_points?.length) {

        analysis.key_points.forEach(point => {

            const li = document.createElement("li");

            li.textContent = point;

            keyPoints.appendChild(li);

        });

    } else {

        keyPoints.innerHTML =
            "<li>No key points identified.</li>";

    }


    /* SENTIMENT */

    if (analysis.sentiment) {

        const label =
            analysis.sentiment.label || "Unknown";

        sentiment.textContent = label;

        sentimentExplanation.textContent =
            analysis.sentiment.explanation || "";

        sentiment.className = "sentiment";

        const sentimentClass =
            label.toLowerCase();

        if (
            ["positive", "negative", "neutral", "mixed"]
            .includes(sentimentClass)
        ) {

            sentiment.classList.add(sentimentClass);

        }

    } else {

        sentiment.textContent = "Unknown";

        sentimentExplanation.textContent = "";

        sentiment.className = "sentiment";

    }


    /* TOPICS */

    topics.innerHTML = "";

    if (analysis.main_topics?.length) {

        analysis.main_topics.forEach(topic => {

            const li = document.createElement("li");

            li.textContent = topic;

            topics.appendChild(li);

        });

    } else {

        topics.innerHTML =
            "<li>No main topics identified.</li>";

    }


    /* ACTION ITEMS */

    actions.innerHTML = "";

    if (analysis.action_items?.length) {

        analysis.action_items.forEach(action => {

            const li = document.createElement("li");

            li.textContent = action;

            actions.appendChild(li);

        });

    } else {

        actions.innerHTML =
            "<li>No action items identified.</li>";

    }

}


/* =========================
   ANALYZE VIDEO
========================= */

uploadButton.addEventListener("click", async () => {

    const file = videoInput.files[0];

    if (!file) {
        return;
    }

    const formData = new FormData();

    formData.append("file", file);

    showLoading();

    results.classList.add("hidden");


    try {

        /*
         * These messages are only UI feedback.
         * The backend performs the actual processing.
         */

        setTimeout(() => {

            if (uploadButton.disabled) {
                status.textContent =
                    "🎙️ Transcribing audio...";
            }

        }, 1000);


        setTimeout(() => {

            if (uploadButton.disabled) {
                status.textContent =
                    "🤖 Analyzing with AI...";
            }

        }, 3000);


        const response = await fetch("/upload", {

            method: "POST",

            body: formData

        });


        if (!response.ok) {

            let message =
                `Server error (${response.status})`;

            try {

                const errorData =
                    await response.json();

                if (errorData.detail) {
                    message = errorData.detail;
                }

            } catch {
                // Keep default error message.
            }

            throw new Error(message);

        }


        const data = await response.json();


        /* TRANSCRIPT */

        transcript.textContent =
            data.transcript ||
            "No transcript available.";


        /* ANALYSIS */

        displayAnalysis(data.analysis || {});


        /* SHOW RESULTS */

        results.classList.remove("hidden");

        results.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });


        setStatus("✅ Analysis complete.");


    } catch (error) {

        console.error(error);

        showError(
            error.message ||
            "Something went wrong while analyzing the video."
        );

    } finally {

        uploadButton.disabled = false;

        uploadButton.textContent =
            "Analyze Video";

    }

});


/* =========================
   COPY TRANSCRIPT
========================= */

copyTranscript.addEventListener("click", async () => {

    try {

        await navigator.clipboard.writeText(
            transcript.textContent
        );

        copyTranscript.textContent = "Copied!";

        setTimeout(() => {

            copyTranscript.textContent =
                "Copy Transcript";

        }, 1500);

    } catch {

        showError(
            "Unable to copy the transcript."
        );

    }

});


/* =========================
   NEW ANALYSIS
========================= */

newAnalysisButton.addEventListener("click", () => {

    videoInput.value = "";

    resetFile();

    results.classList.add("hidden");

    status.textContent = "";

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

});


/* =========================
   DOWNLOAD ANALYSIS
========================= */

downloadAnalysis.addEventListener("click", () => {

    const analysisText = `
VIDEO AUTOPSY — ANALYSIS
========================

SUMMARY
-------
${summary.innerText || "No summary available."}


KEY POINTS
----------
${keyPoints.innerText || "No key points identified."}


SENTIMENT
---------
${sentiment.innerText || "Unknown"}

${sentimentExplanation.innerText || ""}


MAIN TOPICS
-----------
${topics.innerText || "No main topics identified."}


ACTION ITEMS
------------
${actions.innerText || "No action items identified."}


TRANSCRIPT
----------
${transcript.innerText || "No transcript available."}
`;

    const blob = new Blob(
        [analysisText],
        { type: "text/plain" }
    );

    const url =
        URL.createObjectURL(blob);

    const link =
        document.createElement("a");

    link.href = url;

    link.download =
        "video-autopsy-analysis.txt";

    document.body.appendChild(link);

    link.click();

    document.body.removeChild(link);

    URL.revokeObjectURL(url);

});



resetFile();