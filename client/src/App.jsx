// src/App.jsx
import React, { useEffect, useState } from "react";
import "./App.css";
import toast from "react-hot-toast";
import { getContacts, createContact, getMessages, saveMessage, generateMessage } from "./api";

export default function App() {
  const [contacts, setContacts] = useState([]);
  const [selected, setSelected] = useState(null);
  const [messages, setMessages] = useState([]);
  const [gen, setGen] = useState({ type: "intro", hint: "" });
  const [generated, setGenerated] = useState("");
  const [q, setQ] = useState("");
  const [loadingGen, setLoadingGen] = useState(false);
  const [saving, setSaving] = useState(false);

  useEffect(() => { loadContacts(); }, []);

  async function loadContacts() {
    try {
      const data = await getContacts();
      setContacts(Array.isArray(data) ? data : []);
    } catch (e) {
      console.error(e);
      toast.error(`Failed to load contacts: ${e.message}`);
      setContacts([]); // Đảm bảo luôn là array
    }
  }

  async function addContact(ev) {
    ev.preventDefault();
    const payload = Object.fromEntries(new FormData(ev.target).entries());
    try {
      await createContact(payload);
      ev.target.reset();
      await loadContacts();
      toast.success("Contact added");
    } catch (e) {
      toast.error(`Create failed: ${e.message}`);
    }
  }

  async function selectContact(c) {
    setSelected(c);
    setGenerated("");
    try {
      setMessages((await getMessages(c.id)) || []);
    } catch {
      setMessages([]);
      toast.error("Failed to load messages");
    }
  }

  async function onGenerate() {
    if (!selected) {
      toast("Pick a contact first", { icon: "👀" });
      return;
    }
    try {
      setLoadingGen(true);
      const res = await generateMessage({
        contact_id: selected.id,
        message_type: gen.type,
        prompt_hint: gen.hint || undefined
      });
      setGenerated(res.content || res.response || "");
      await refreshMessages();
      toast.success("Draft generated");
    } catch (e) {
      toast.error(`Generate failed: ${e.message}`);
    } finally {
      setLoadingGen(false);
    }
  }

  async function refreshMessages() {
    if (!selected) return;
    setMessages((await getMessages(selected.id)) || []);
  }

  async function onSave() {
    if (!selected || !generated.trim()) {
      toast("Nothing to save", { icon: "📝" });
      return;
    }
    try {
      setSaving(true);
      await saveMessage(selected.id, { message_type: gen.type, content: generated });
      await refreshMessages();
      toast.success("Saved");
    } catch (e) {
      toast.error(`Save failed: ${e.message}`);
    } finally {
      setSaving(false);
    }
  }

  const filtered = contacts.filter(c => {
    const s = (q || "").toLowerCase();
    return !s || [c.name, c.email, c.company, c.role].some(v => (v || "").toLowerCase().includes(s));
  });

  // Hàm xuất CSV
  function exportMessagesCSV() {
    if (!messages.length) {
      toast("No messages to export", { icon: "📭" });
      return;
    }
    const header = ["ID", "Type", "Content"];
    const rows = messages.map(m => [m.id, m.message_type, m.content.replace(/\r?\n|\r/g, " ")]);
    const csv = [header, ...rows]
      .map(row => row.map(field => `"${String(field).replace(/"/g, '""')}"`).join(","))
      .join("\n");
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${selected?.name || "messages"}_messages.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    toast.success("CSV exported");
  }

  return (
    <div className="app">
      <header className="app__bar">
        <div className="brand">AI-Powered Outreach System</div>
        <input
          className="input input--search"
          placeholder="Search contacts…"
          value={q}
          onChange={e => setQ(e.target.value)}
        />
      </header>

      <main className="grid">
        {/* LEFT */}
        <section className="card card--tall">
          <div className="card__title">Contacts</div>

          <form className="form" onSubmit={addContact}>
            <input name="name" className="input" placeholder="Name" required />
            <input name="email" className="input" placeholder="Email" />
            <div className="grid--2">
              <input name="company" className="input" placeholder="Company" />
              <input name="role" className="input" placeholder="Role" />
            </div>
            <button type="submit" className="btn btn--primary">Add</button>
          </form>

          <ul className="list">
            {filtered.map(c => (
              <li
                key={c.id}
                className={`list__item ${selected?.id === c.id ? "is-active" : ""}`}
                onClick={() => selectContact(c)}
                title={c.email || ""}
              >
                <div className="avatar">{(c.name || "?").charAt(0).toUpperCase()}</div>
                <div className="list__meta">
                  <div className="list__title">{c.name}</div>
                  <div className="list__sub">
                    {c.company || "—"} {c.role ? `• ${c.role}` : ""}
                  </div>
                </div>
              </li>
            ))}
            {!filtered.length && <li className="empty">No contacts found.</li>}
          </ul>
        </section>

        {/* RIGHT */}
        <section className="card card--tall">
          <div className="card__title" style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
            <span>Messages</span>
            <button
              className="btn btn--small"
              style={{ marginLeft: 8 }}
              onClick={exportMessagesCSV}
              disabled={!messages.length}
              type="button"
              title="Export messages to CSV"
            >
              Export CSV
            </button>
          </div>

          <div className="contact__badge">
            {selected ? (
              <>
                <span className="badge__name">{selected.name}</span>
                <span className="badge__sep">—</span>
                <span className="badge__email">{selected.email || "no email"}</span>
              </>
            ) : (
              <span className="muted">No contact selected</span>
            )}
          </div>

          {!selected ? (
            <div className="empty mt">Pick a contact to start composing.</div>
          ) : (
            <>
              <div className="compose">
                <label className="field">
                  <span className="field__label">Type</span>
                  <select
                    className="input"
                    value={gen.type}
                    onChange={e => setGen(s => ({ ...s, type: e.target.value }))}
                  >
                    <option value="intro">Intro</option>
                    <option value="followup">Follow-up</option>
                    <option value="meeting">Meeting</option>
                  </select>
                </label>

                <label className="field">
                  <span className="field__label">Prompt hint</span>
                  <input
                    className="input"
                    placeholder="e.g., mention last week’s conference"
                    value={gen.hint}
                    onChange={e => setGen(s => ({ ...s, hint: e.target.value }))}
                    onKeyDown={(e) => { if (e.key === "Enter") onGenerate(); }}
                  />
                </label>

                <div className="row">
                  <button
                    className={`btn btn--primary ${loadingGen ? "btn--loading" : ""}`}
                    onClick={onGenerate}
                    disabled={loadingGen}
                    type="button"
                  >
                    {loadingGen ? "Generating…" : "Generate"}
                  </button>
                  <button className="btn" onClick={() => setGenerated("")} type="button">Clear</button>
                </div>
              </div>

              <div className="generated">
                <div className="section__title">Generated</div>
                <textarea
                  className="textarea"
                  rows={8}
                  value={generated}
                  placeholder="Your AI-generated draft will appear here"
                  onChange={e => setGenerated(e.target.value)}
                />
                <div className="row">
                  <button
                    className={`btn btn--success ${saving ? "btn--loading" : ""}`}
                    onClick={onSave}
                    disabled={!generated.trim() || saving}
                    type="button"
                  >
                    {saving ? "Saving…" : "Save Draft"}
                  </button>
                </div>
              </div>

              <div className="history">
                <div className="section__title">History</div>
                <ul className="timeline">
                  {messages.length === 0 && <li className="empty">No messages yet.</li>}
                  {messages.map(m => (
                    <li key={m.id} className="timeline__item">
                      <span className="tag">{m.message_type}</span>
                      <span className="timeline__content">{m.content}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </>
          )}
        </section>
      </main>
    </div>
  );
}
