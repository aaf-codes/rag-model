const API_BASE = "http://127.0.0.1:8000";

// LOAD PAPERS
async function loadPapers() {

    try {

        const response =
            await fetch(`${API_BASE}/papers`);

        const data =
            await response.json();

        const papersList =
            document.getElementById("papersList");

        papersList.innerHTML = "";

        if (data.papers.length === 0) {

            papersList.innerHTML =
                `
                <p style="color:#94a3b8;">
                    No papers uploaded yet
                </p>
                `;

            return;
        }

        data.papers.forEach((paper) => {

            papersList.innerHTML += `
                <div class="paper-card">

                    <h4>
                        📄 ${paper}
                    </h4>

                    <button
                        class="delete-btn"
                        onclick="deletePaper('${paper}')"
                    >
                        Delete
                    </button>

                </div>
            `;
        });

    } catch (error) {

        console.error(error);

    }
}

// UPLOAD MULTIPLE PDFs
async function uploadPDF() {

    const fileInput =
        document.getElementById("pdfFile");

    const files =
        fileInput.files;

    if (files.length === 0) {

        alert("Please select PDFs");

        return;
    }

    const uploadStatus =
        document.getElementById("uploadStatus");

    uploadStatus.innerHTML =
        `
        Uploading ${files.length} PDFs...
        `;

    for (let i = 0; i < files.length; i++) {

        const file = files[i];

        uploadStatus.innerHTML =
            `
            Uploading:
            <b>${file.name}</b>
            (${i + 1}/${files.length})
            `;

        const formData = new FormData();

        formData.append("file", file);

        try {

            await fetch(
                `${API_BASE}/upload-paper`,
                {
                    method: "POST",
                    body: formData
                }
            );

        } catch (error) {

            console.error(error);

        }
    }

    uploadStatus.innerHTML =
        `
        ✅ All PDFs uploaded successfully
        `;

    loadPapers();
}

// DELETE PAPER
async function deletePaper(filename) {

    const confirmDelete =
        confirm(`Delete ${filename}?`);

    if (!confirmDelete) return;

    try {

        const response =
            await fetch(
                `${API_BASE}/delete-paper/${filename}`,
                {
                    method: "DELETE"
                }
            );

        const data =
            await response.json();

        alert(data.message);

        loadPapers();

    } catch (error) {

        console.error(error);

    }
}

// GENERATE SUMMARY
async function generateSummary() {

    const query =
        document.getElementById("queryInput").value;

    if (!query) {

        alert("Enter research query");

        return;
    }

    document.getElementById("summaryOutput")
        .innerHTML =
        `
        ⏳ Generating AI summary...
        `;

    document.getElementById("sourcePapers")
        .innerHTML =
        `
        Loading source papers...
        `;

    document.getElementById("retrievedChunks")
        .innerHTML =
        `
        Retrieving semantic chunks...
        `;

    try {

        const response =
            await fetch(
                `${API_BASE}/query`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                        "application/json"
                    },

                    body: JSON.stringify({
                        query: query
                    })
                }
            );

        const data =
            await response.json();

        // SUMMARY
        document.getElementById("summaryOutput")
            .innerHTML =
            data.summary;

        // SOURCE PAPERS
        document.getElementById("sourcePapers")
            .innerHTML =
            data.source_papers
                .map(
                    paper =>
                    `📄 ${paper}`
                )
                .join("<br><br>");

        // RETRIEVED CHUNKS
        document.getElementById("retrievedChunks")
            .innerHTML =
            data.retrieved_chunks
                .map(
                    chunk =>
                    `<p>${chunk}</p>`
                )
                .join("<hr>");

    } catch (error) {

        console.error(error);

    }
}

// INITIAL LOAD
loadPapers();