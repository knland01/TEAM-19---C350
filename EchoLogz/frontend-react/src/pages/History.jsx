// src/pages/History.jsx
import React from "react";
import "../style_history.css";

export default function History() {
  return (
    <div className="wrap">
      <div className="topbar">
        <div className="brand">
          <div className="logo">EL</div>
          <div>
            <div className="title">EchoLogz</div>
            <div className="muted">History / Saved Comparisons</div>
          </div>
        </div>

        <div className="controls">
          <button className="btn">Dashboard</button>
          <button className="btn">New Compare</button>
          <button className="btn primary">Export CSV</button>
        </div>
      </div>

      <div className="panel">
        <div className="filters">
          <input
            id="q"
            className="input"
            placeholder="Search user, tag, playlist…"
          />
          <select id="status">
            <option value="">All Status</option>
            <option value="ok">Complete</option>
            <option value="warn">Partial</option>
            <option value="err">Failed</option>
          </select>
          <input id="from" type="date" className="input" />
          <input id="to" type="date" className="input" />
        </div>

        <div className="chips" id="chips">
          <div className="chip active" data-chip="all">
            All
          </div>
          <div className="chip" data-chip="me">
            Me vs Others
          </div>
          <div className="chip" data-chip="group">
            Group
          </div>
          <div className="chip" data-chip="playlist">
            Playlist vs Playlist
          </div>
          <div className="chip" data-chip="high">
            Score ≥ 0.75
          </div>
        </div>

        <div
          id="tableWrap"
          className="panel"
          style={{ padding: 0, marginTop: 16 }}
        >
          <table className="table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Participants</th>
                <th>Type</th>
                <th>Score</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>

            {/* empty body for now; logic comes later */}
            <tbody id="rows"></tbody>
          </table>

          <div id="empty" className="empty" style={{ display: "none" }}>
            No results match your filters.
          </div>

          <div className="footer">
            <div id="count" className="muted">
              0 results
            </div>
            <div className="pager">
              <button className="btn" id="prev">
                Prev
              </button>
              <button className="btn" id="next">
                Next
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Drawer / details mock */}
      <aside id="drawer" className="drawer" aria-hidden="true">
        <h3>Compare Details</h3>
        <div className="muted" id="pairId">
          Pair #—
        </div>
        <div className="divider"></div>
        <div className="kv">
          <span>Date:</span> <strong id="dDate">—</strong>
        </div>
        <div className="kv">
          <span>Participants:</span> <strong id="dUsers">—</strong>
        </div>
        <div className="kv">
          <span>Type:</span> <strong id="dType">—</strong>
        </div>
        <div className="kv">
          <span>Score:</span> <strong id="dScore">—</strong>
        </div>
        <div className="kv">
          <span>Status:</span> <strong id="dStatus">—</strong>
        </div>
        <div className="divider"></div>
        <div className="kv">
          <span>Top shared genres:</span>
          <strong>Indie, Alt Rock, Chill</strong>
        </div>
        <div className="kv">
          <span>Notes:</span>
          <strong>Sample of 100 tracks per user</strong>
        </div>
        <div className="divider"></div>
        <div className="actions">
          <button className="mini view">Open Heatmap</button>
          <button className="mini rerun">Re-run</button>
          <button className="mini del">Delete</button>
          <button id="closeDrawer" className="mini">
            Close
          </button>
        </div>
      </aside>
    </div>
  );
}