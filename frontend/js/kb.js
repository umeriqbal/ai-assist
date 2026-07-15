import { apiPostForm, apiPost } from "./api.js";

const uploadForm = document.getElementById("upload-form");
const uploadFileInput = document.getElementById("upload-file");
const uploadSourceInput = document.getElementById("upload-source");
const uploadResultEl = document.getElementById("upload-result");

const searchForm = document.getElementById("search-form");
const searchQueryInput = document.getElementById("search-query");
const searchResultsEl = document.getElementById("search-results");

uploadForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const file = uploadFileInput.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("file", file);
  if (uploadSourceInput.value.trim()) {
    formData.append("source", uploadSourceInput.value.trim());
  }

  uploadResultEl.innerHTML = "";
  uploadResultEl.className = "kb-notice kb-notice-pending";
  uploadResultEl.textContent = "Uploading…";

  try {
    const result = await apiPostForm("/documents/upload", formData);

    uploadResultEl.className = "kb-notice kb-notice-ok";
    uploadResultEl.textContent =
      `Indexed "${result.source}" — ${result.pages_loaded} page(s), ` +
      `${result.chunks_indexed} chunk(s).`;

    uploadForm.reset();
  } catch (error) {
    uploadResultEl.className = "kb-notice kb-notice-error";
    uploadResultEl.textContent = `Error: ${error.message}`;
  }
});

searchForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const query = searchQueryInput.value.trim();
  if (!query) return;

  searchResultsEl.className = "kb-results";
  searchResultsEl.textContent = "Searching…";

  try {
    const result = await apiPost("/documents/search", { query, k: 4 });

    searchResultsEl.innerHTML = "";

    if (result.results.length === 0) {
      searchResultsEl.textContent = "No results.";
      return;
    }

    for (const item of result.results) {
      const card = document.createElement("div");
      card.className = "kb-result";

      const meta = document.createElement("div");
      meta.className = "kb-result-meta";

      const source = document.createElement("span");
      source.className = "kb-result-source";
      source.textContent = item.metadata?.source ?? "unknown source";

      const score = document.createElement("span");
      score.className = "kb-result-score";
      score.textContent = `score ${item.score.toFixed(3)}`;

      meta.append(source, score);

      const content = document.createElement("p");
      content.className = "kb-result-content";
      content.textContent = item.content;

      card.append(meta, content);
      searchResultsEl.append(card);
    }
  } catch (error) {
    searchResultsEl.innerHTML = "";
    searchResultsEl.className = "kb-notice kb-notice-error";
    searchResultsEl.textContent = `Error: ${error.message}`;
  }
});
