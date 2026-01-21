export class ApiClient {
  constructor({ baseUrl }) {
    this.baseUrl = baseUrl;
  }

  async fetchProfiles(signal) {
    return this.#requestJson("/profiles", { method: "GET", signal });
  }

  async generateThought(payload, signal) {
    return this.#requestJson("/generate", {
      method: "POST",
      signal,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
  }

  async resolveConflict(payload, signal) {
    return this.#requestJson("/resolve-conflict", {
      method: "POST",
      signal,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
  }

  async #requestJson(path, options) {
    const response = await fetch(`${this.baseUrl}${path}`, options);
    const data = await response.json().catch(() => ({
      error: {
        error_code: "INTERNAL_ERROR",
        message: "Invalid JSON response",
        hint: "Check backend logs",
        span: null
      }
    }));

    if (!response.ok) {
      return Promise.reject(data);
    }

    if (data?.error) {
      return Promise.reject(data);
    }

    return data;
  }
}
