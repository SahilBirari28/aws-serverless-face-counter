const config = window.APP_CONFIG || {};
const API_URL = (config.API_URL || "").replace(/\/$/, "");

const imageInput = document.getElementById("imageInput");
const preview = document.getElementById("preview");
const uploadButton = document.getElementById("uploadButton");
const statusBox = document.getElementById("status");
const resultBox = document.getElementById("resultBox");
const faceCountBox = document.getElementById("faceCount");

imageInput.addEventListener("change", () => {
    const file = imageInput.files[0];

    resultBox.style.display = "none";
    statusBox.textContent = "";

    if (!file) {
        preview.style.display = "none";
        return;
    }

    preview.src = URL.createObjectURL(file);
    preview.style.display = "block";
});

uploadButton.addEventListener("click", uploadImage);

async function uploadImage() {
    const file = imageInput.files[0];

    if (!API_URL || API_URL.includes("YOUR-API-ID")) {
        statusBox.textContent = "❌ Configure API_URL in frontend/config.js first.";
        return;
    }

    if (!file) {
        statusBox.textContent = "❌ Please select an image first.";
        return;
    }

    if (!["image/jpeg", "image/png"].includes(file.type)) {
        statusBox.textContent = "❌ Only JPG, JPEG and PNG images are supported.";
        return;
    }

    try {
        setLoading(true);
        resultBox.style.display = "none";

        statusBox.textContent = "Getting secure upload URL...";

        const urlResponse = await fetch(`${API_URL}/upload-url`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                filename: file.name,
                contentType: file.type
            })
        });

        if (!urlResponse.ok) {
            const text = await urlResponse.text();
            throw new Error(`Upload URL request failed (${urlResponse.status}): ${text}`);
        }

        const data = await urlResponse.json();

        statusBox.textContent = "Uploading image to Amazon S3...";

        const uploadResponse = await fetch(data.uploadUrl, {
            method: "PUT",
            headers: {
                "Content-Type": file.type
            },
            body: file
        });

        if (!uploadResponse.ok) {
            const text = await uploadResponse.text();
            console.error("S3 upload response:", text);
            throw new Error(`S3 upload failed (${uploadResponse.status}). Check the browser console.`);
        }

        statusBox.textContent = "Image uploaded. Detecting faces...";

        await pollForResult(data.key);
    } catch (error) {
        console.error(error);
        statusBox.textContent = `❌ ${error.message}`;
        setLoading(false);
    }
}

async function pollForResult(imageKey) {
    for (let attempt = 0; attempt < 30; attempt++) {
        const response = await fetch(
            `${API_URL}/result?key=${encodeURIComponent(imageKey)}`
        );

        if (!response.ok) {
            throw new Error(`Unable to check result (${response.status}).`);
        }

        const data = await response.json();

        if (data.status === "completed") {
            faceCountBox.textContent = data.faceCount;
            resultBox.style.display = "block";
            statusBox.textContent = "✅ Face detection completed!";
            setLoading(false);
            return;
        }

        if (data.status === "failed") {
            throw new Error(data.error || "Face detection failed.");
        }

        statusBox.textContent = "🔍 Amazon Rekognition is analysing the image...";
        await sleep(1000);
    }

    throw new Error("Detection took too long. Please try again.");
}

function setLoading(isLoading) {
    uploadButton.disabled = isLoading;
    uploadButton.textContent = isLoading
        ? "Processing..."
        : "Upload & Detect Faces";
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
