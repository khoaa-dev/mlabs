// client/src/api.js
import axios from "axios";

const api = axios.create({
  baseURL: "/", // Vite proxy will forward /contacts and /messages to :8000
  headers: { "Content-Type": "application/json" },
});

// one helper for consistency
async function request(path, opts = {}) {
  try {
    const res = await api({ url: path, ...opts });
    return res.data ?? null;
  } catch (err) {
    // Treat 404 on GET as "no data" so UI can show an empty state
    if (err.response && err.response.status === 404 && (!opts.method || opts.method === "GET")) {
      return null;
    }
    if (err.response) throw new Error(`${err.response.status} ${err.response.data}`);
    throw err;
  }
}

export const getContacts = () => request("/contacts");

export const createContact = (payload) =>
  request("/contacts", { method: "POST", data: payload });

export const getMessages = (cid) =>
  request(`/messages/contact/${cid}`);

export const saveMessage = (cid, payload) =>
  request(`/messages/contact/${cid}`, { method: "POST", data: payload });

export const generateMessage = (payload) =>
  request("/messages/preview", { method: "POST", data: payload });
