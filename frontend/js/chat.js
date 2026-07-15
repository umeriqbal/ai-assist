import { apiPostStream } from "./api.js";

const messagesEl = document.getElementById("chat-messages");
const formEl = document.getElementById("chat-form");
const inputEl = document.getElementById("chat-input");
const sendEl = document.getElementById("chat-send");

function appendMessage(role) {
  const bubble = document.createElement("div");
  bubble.className = `chat-bubble chat-bubble-${role}`;
  messagesEl.append(bubble);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return bubble;
}

function setSending(isSending) {
  inputEl.disabled = isSending;
  sendEl.disabled = isSending;
}

async function sendMessage(prompt) {
  appendMessage("user").textContent = prompt;

  const assistantBubble = appendMessage("assistant");
  assistantBubble.classList.add("chat-bubble-pending");

  setSending(true);

  try {
    let firstChunk = true;

    await apiPostStream("/chat/stream", { prompt }, (chunk) => {
      if (firstChunk) {
        assistantBubble.classList.remove("chat-bubble-pending");
        firstChunk = false;
      }
      assistantBubble.textContent += chunk;
      messagesEl.scrollTop = messagesEl.scrollHeight;
    });
  } catch (error) {
    assistantBubble.classList.remove("chat-bubble-pending");
    assistantBubble.classList.add("chat-bubble-error");
    assistantBubble.textContent = `Error: ${error.message}`;
  } finally {
    setSending(false);
    inputEl.focus();
  }
}

formEl.addEventListener("submit", (event) => {
  event.preventDefault();

  const prompt = inputEl.value.trim();
  if (!prompt) return;

  inputEl.value = "";
  sendMessage(prompt);
});

inputEl.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    formEl.requestSubmit();
  }
});
