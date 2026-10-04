async function uploadDocument() {

    const fileInput =
        document.getElementById("documentFile");

    const status =
        document.getElementById("uploadStatus");

    if (!fileInput.files.length) {

        status.innerText =
            "Please select at least one document.";

        return;
    }

    const files = fileInput.files;

    const formData = new FormData();

    for (let i = 0; i < files.length; i++) {

        formData.append(
            "files",
            files[i]
        );
    }

    status.innerText =
        `Processing ${files.length} document(s)...`;

    try {

        const response = await fetch(
            "/upload",
            {
                method: "POST",
                body: formData
            }
        );

        const data =
            await response.json();

        if (!response.ok) {

            status.innerText =
                data.error ||
                "Upload failed.";

            return;
        }

        const fileNames =
            data.files.join(", ");

        status.innerText =
            `${data.files.length} document(s) processed successfully. ` +
            `${data.chunks} chunks created.`;

        addMessage(
            "system-message",
            `Documents ready: ${fileNames}`
        );

    } catch (error) {

        status.innerText =
            "Error: " + error.message;

        console.error(error);
    }
}


async function askQuestion() {

    const input =
        document.getElementById(
            "questionInput"
        );

    const question =
        input.value.trim();

    if (!question) {
        return;
    }

    addMessage(
        "user-message",
        question
    );

    input.value = "";

    addMessage(
        "system-message",
        "Searching documents..."
    );

    try {

        const response =
            await fetch(
                "/ask",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        question:
                            question
                    })
                }
            );

        const data =
            await response.json();

        removeLastMessage();

        if (!response.ok) {

            addMessage(
                "system-message",
                data.error ||
                "Unable to process the question."
            );

            return;
        }

        let answerHTML = `
            <strong>Answer</strong>

            <p>
                ${escapeHTML(data.answer)}
            </p>
        `;


        /*
         * Chat history information
         */

        if (
            typeof data.chat_history_length
            === "number"
        ) {

            answerHTML += `
                <div class="source">
                    Conversation Turn:
                    ${data.chat_history_length}
                </div>
            `;
        }


        /*
         * Retrieved sources
         */

        if (
            data.sources &&
            data.sources.length > 0
        ) {

            answerHTML += `
                <div class="source">

                    <strong>
                        Retrieved Sources
                    </strong>

                    <ul>
            `;

            data.sources.forEach(
                (source, index) => {

                    const score =
                        typeof source.score ===
                        "number"
                            ? source.score.toFixed(4)
                            : "N/A";

                    const documentName =
                        source.document ||
                        "Unknown document";

                    answerHTML += `
                        <li>

                            Source ${index + 1}
                            —

                            Document:
                            ${escapeHTML(
                                documentName
                            )}

                            ,

                            Page:
                            ${source.page}

                            ,

                            Chunk:
                            ${source.chunk_id}

                            ,

                            Relevance Score:
                            ${score}

                        </li>
                    `;
                }
            );

            answerHTML += `
                    </ul>

                </div>
            `;
        }


        /*
         * Retrieved context
         */

        if (
            data.retrieved_chunks &&
            data.retrieved_chunks.length > 0
        ) {

            answerHTML += `
                <details
                    class="retrieved-details"
                >

                    <summary>
                        View Retrieved Context
                    </summary>
            `;

            data.retrieved_chunks.forEach(
                (result, index) => {

                    const chunk =
                        result.chunk;

                    const score =
                        typeof result.reranker_score
                        === "number"

                            ? result.reranker_score
                                .toFixed(4)

                            : "N/A";

                    const documentName =
                        chunk.source ||
                        "Unknown document";

                    answerHTML += `
                        <div
                            class="retrieved-chunk"
                        >

                            <strong>
                                Result ${index + 1}
                            </strong>

                            <p>
                                ${escapeHTML(
                                    chunk.text
                                )}
                            </p>

                            <small>

                                Document:
                                ${escapeHTML(
                                    documentName
                                )}

                                |

                                Page:
                                ${chunk.page}

                                |

                                Chunk:
                                ${chunk.chunk_id}

                                |

                                Reranker Score:
                                ${score}

                            </small>

                        </div>
                    `;
                }
            );

            answerHTML += `
                </details>
            `;
        }


        addMessage(
            "answer-message",
            answerHTML,
            true
        );

    } catch (error) {

        removeLastMessage();

        addMessage(
            "system-message",
            "Server error. Please try again."
        );

        console.error(error);
    }
}


function addMessage(
    className,
    content,
    isHTML = false
) {

    const chatBox =
        document.getElementById(
            "chatBox"
        );

    const message =
        document.createElement("div");

    message.className =
        `message ${className}`;

    if (isHTML) {

        message.innerHTML =
            content;

    } else {

        message.innerText =
            content;
    }

    chatBox.appendChild(
        message
    );

    chatBox.scrollTop =
        chatBox.scrollHeight;
}


function removeLastMessage() {

    const chatBox =
        document.getElementById(
            "chatBox"
        );

    if (chatBox.lastElementChild) {

        chatBox.removeChild(
            chatBox.lastElementChild
        );
    }
}


function handleEnter(event) {

    if (event.key === "Enter") {

        askQuestion();
    }
}


function escapeHTML(text) {

    const div =
        document.createElement(
            "div"
        );

    div.innerText =
        text;

    return div.innerHTML;
}