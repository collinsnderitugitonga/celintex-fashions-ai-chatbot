const API_URL = "http://127.0.0.1:8000/api/chat";

// Open the AI chat section
function openChat() {
    const chatSection = document.getElementById("ai-assistant");

    if (chatSection) {
        chatSection.scrollIntoView({
            behavior: "smooth"
        });

        setTimeout(() => {
            const input = document.getElementById("chat-input");

            if (input) {
                input.focus();
            }
        }, 600);
    }
}


// Add a message to the chat
function addMessage(message, type) {
    const messagesContainer = document.getElementById("chat-messages");

    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message");

    if (type === "user") {
        messageDiv.classList.add("user-message");
    } else {
        messageDiv.classList.add("assistant-message");
    }

    messageDiv.innerHTML = message.replace(/\n/g, "<br>");

    messagesContainer.appendChild(messageDiv);

    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}


// Show loading message
function showLoading() {
    const messagesContainer = document.getElementById("chat-messages");

    const loadingDiv = document.createElement("div");
    loadingDiv.classList.add("message", "assistant-message");
    loadingDiv.id = "loading-message";

    loadingDiv.innerHTML = "Celintex AI is thinking...";

    messagesContainer.appendChild(loadingDiv);

    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}


// Remove loading message
function removeLoading() {
    const loadingMessage = document.getElementById("loading-message");

    if (loadingMessage) {
        loadingMessage.remove();
    }
}


// Send message to FastAPI
async function sendMessage(message) {
    try {
        showLoading();

        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        removeLoading();

        if (!response.ok) {
            throw new Error("Server returned an error.");
        }

        const data = await response.json();

        addMessage(data.response, "assistant");

    } catch (error) {
        removeLoading();

        console.error("Chat error:", error);

        addMessage(
            "Sorry, I'm having trouble connecting to the Celintex AI right now. Please try again or contact us at 0722285544.",
            "assistant"
        );
    }
}


// Handle chat form submission
document.addEventListener("DOMContentLoaded", function () {

    const chatForm = document.getElementById("chat-form");
    const chatInput = document.getElementById("chat-input");

    if (!chatForm || !chatInput) {
        return;
    }

    chatForm.addEventListener("submit", function (event) {

        event.preventDefault();

        const message = chatInput.value.trim();

        if (!message) {
            return;
        }

        // Display user's message
        addMessage(message, "user");

        // Clear input
        chatInput.value = "";

        // Send to AI
        sendMessage(message);
    });

});

// Mobile navigation menu
const menuToggle = document.getElementById("menu-toggle");
const navLinks = document.querySelector(".nav-links");

if (menuToggle && navLinks) {
    menuToggle.addEventListener("click", function () {
        navLinks.classList.toggle("active");

        if (navLinks.classList.contains("active")) {
            menuToggle.innerHTML = "✕";
            menuToggle.setAttribute("aria-label", "Close navigation menu");
        } else {
            menuToggle.innerHTML = "☰";
            menuToggle.setAttribute("aria-label", "Open navigation menu");
        }
    });


    // Close menu after clicking a navigation link
    navLinks.querySelectorAll("a").forEach(function (link) {
        link.addEventListener("click", function () {
            navLinks.classList.remove("active");
            menuToggle.innerHTML = "☰";
            menuToggle.setAttribute("aria-label", "Open navigation menu");
        });
    });
}
