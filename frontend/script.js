// SMART LINK: Automatically switches between your laptop and the real internet
const API_BASE = window.location.hostname === "127.0.0.1" || window.location.hostname === "localhost"
    ? "http://127.0.0.1:8000"
    : window.location.origin;

// LOAD PAPERS
async function loadPapers() {
    try {
        // FIXED ADDRESS: Changed /list-papers to /papers to fix the backend 404 error
        const response = await fetch(`${API_BASE}/papers`);
        const data = await response.json();
        console.log("PAPERS API RAW DATA:", JSON.stringify(data));

        const papersList = document.getElementById("papersList");
        
        // SAFE CLEANUP: Erases old items without using vulnerable innerHTML
        papersList.replaceChildren();

        // BULLETPROOF CHECK: Handles data if it's a raw list OR an object with a .papers key
        const papersArray = Array.isArray(data) ? data : (data.papers || []);

        // EMPTY CHECK
        if (papersArray.length === 0) {
            const emptyMessage = document.createElement("p");
            emptyMessage.textContent = "No papers uploaded yet";
            papersList.appendChild(emptyMessage);
            return;
        }

        // DISPLAY PAPERS - UPDATED WITH TRAINER'S EXACT DESTRUCTURING STRUCTURE
        papersArray.forEach(item => {
            const filename = item.paper;
            const label = item.title || filename;
            const authors = item.authors ? ` — ${item.authors}` : "";
            const year = item.year ? ` (${item.year})` : "";

            const card = document.createElement("div");
            card.className = "paper-card";

            // Retaining your beautiful layout styles on the new card variable
            card.style.background = "white";
            card.style.border = "1px solid #dbeafe";
            card.style.padding = "15px";
            card.style.marginTop = "12px";
            card.style.borderRadius = "12px";
            card.style.color = "black";

            const title = document.createElement("h4");
            // Combines everything cleanly on one line using the requested pattern
            title.textContent = `📄 ${label}${authors}${year}`;
            title.style.marginBottom = "8px";

            const btn = document.createElement("button");
            btn.className = "delete-btn";
            btn.textContent = "Delete";
            
            // Layout styling for the button
            btn.style.marginTop = "10px";
            btn.style.background = "#2563eb";
            btn.style.color = "white";
            btn.style.border = "none";
            btn.style.padding = "8px 12px";
            btn.style.borderRadius = "8px";
            btn.style.cursor = "pointer";
            
            // Uses standard addEventListener as requested to trigger backend delete safely
            btn.addEventListener("click", () => deletePaper(filename));

            // Append everything together securely
            card.appendChild(title);
            card.appendChild(btn);
            papersList.appendChild(card);
        });

    } catch (error) {
        console.error("LOAD PAPERS ERROR:", error);
    }
}

// UPLOAD PDFs
async function uploadPDF() {
    const fileInput = document.getElementById("pdfFile");
    const files = fileInput.files;

    if (files.length === 0) {
        alert("Select PDFs first");
        return;
    }

    const uploadStatus = document.getElementById("uploadStatus");

    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        
        // SAFE UPDATE: Displays the exact filename securely without execution risks
        uploadStatus.textContent = `Uploading: ${file.name}...`;

        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch(`${API_BASE}/upload-paper`, {
                method: "POST",
                body: formData
            });

            // DUPLICATE PDF CHECK
            if (response.status === 409) {
                const errorData = await response.json();
                alert(errorData.detail);
                continue;
            }

            const data = await response.json();
            console.log("UPLOAD RESPONSE:", data);

        } catch (error) {
            console.error("UPLOAD ERROR:", error);
        }
    }

    uploadStatus.textContent = "✅ Upload completed";

    // RELOAD PAPERS
    await loadPapers();
}

// DELETE PAPER
async function deletePaper(filename) {
    const confirmDelete = confirm(`Delete ${filename}?`);
    if (!confirmDelete) return;

    try {
        const response = await fetch(`${API_BASE}/delete-paper/${filename}`, {
            method: "DELETE"
        });

        const data = await response.json();
        alert(data.message);

        loadPapers();
    } catch (error) {
        console.error(error);
    }
}

// GENERATE SUMMARY
async function generateSummary() {
    const query = document.getElementById("queryInput").value;

    if (!query) {
        alert("Enter research query");
        return;
    }

    document.getElementById("summaryOutput").textContent = "Generating AI summary...";

    try {
        const response = await fetch(`${API_BASE}/query`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                query: query
            })
        });

        const data = await response.json();
        console.log("QUERY RESPONSE:", data);

        // SAFE SUMMARY RENDERING
        document.getElementById("summaryOutput").textContent = data.summary;

        // SOURCE PAPERS
        const sourcePapers = document.getElementById("sourcePapers");
        sourcePapers.replaceChildren();

        data.source_papers.forEach((paper) => {
            const p = document.createElement("p");
            p.textContent = `📄 ${paper}`;
            sourcePapers.appendChild(p);
        });

        // RETRIEVED CHUNKS
        const retrievedChunks = document.getElementById("retrievedChunks");
        retrievedChunks.replaceChildren();

        data.retrieved_chunks.forEach((chunk) => {
            const p = document.createElement("p");
            p.textContent = chunk;
            retrievedChunks.appendChild(p);

            const hr = document.createElement("hr");
            retrievedChunks.appendChild(hr);
        });

    } catch (error) {
        console.error("QUERY ERROR:", error);
    }
}

// INITIAL LOAD
loadPapers();