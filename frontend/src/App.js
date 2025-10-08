import React, { useEffect, useState } from 'react';
import axios from 'axios';

const API = "http://127.0.0.1:8000"; // change if backend runs elsewhere

function App() {
  const [form, setForm] = useState({ species: '', quantity: '', lat: '', lon: '' });
  const [catches, setCatches] = useState([]);
  const [hotspots, setHotspots] = useState([]);

  async function fetchCatches() {
    try {
      const res = await axios.get(`${API}/catches/`);
      setCatches(res.data);
    } catch (err) {
      console.error('Error fetching catches:', err);
    }
  }

  async function fetchHotspots() {
    try {
      const res = await axios.get(`${API}/hotspots/`);
      setHotspots(res.data);
    } catch (err) {
      console.error('Error fetching hotspots:', err);
    }
  }

  async function submitCatch(e) {
    e.preventDefault();
    try {
      await axios.post(`${API}/catches/`, { ...form, fisherman_id: 1 });
      alert('Catch logged successfully!');
      setForm({ species: '', quantity: '', lat: '', lon: '' });
      fetchCatches();
      fetchHotspots();
    } catch (err) {
      alert('Error logging catch');
      console.error(err);
    }
  }

  useEffect(() => {
    fetchCatches();
    fetchHotspots();
  }, []);

  return (
    <div style={{ padding: 20, fontFamily: 'Arial' }}>
      <h1>BioCatch — MVP</h1>

      <div style={{ display: 'flex', gap: 40 }}>
        {/* ----------- Left Section: Form + Recent Catches ----------- */}
        <div style={{ flex: 1 }}>
          <h3>Log Catch</h3>
          <form onSubmit={submitCatch}>
            <div>
              <label>Species: </label>
              <input
                value={form.species}
                onChange={(e) => setForm({ ...form, species: e.target.value })}
                required
              />
            </div>

            <div>
              <label>Quantity: </label>
              <input
                type="number"
                value={form.quantity}
                onChange={(e) => setForm({ ...form, quantity: parseInt(e.target.value) })}
                required
              />
            </div>

            <div>
              <label>Latitude: </label>
              <input
                value={form.lat}
                onChange={(e) => setForm({ ...form, lat: parseFloat(e.target.value) })}
                required
              />
            </div>

            <div>
              <label>Longitude: </label>
              <input
                value={form.lon}
                onChange={(e) => setForm({ ...form, lon: parseFloat(e.target.value) })}
                required
              />
            </div>

            <button type="submit" style={{ marginTop: 10 }}>Submit</button>
          </form>

          <h3 style={{ marginTop: 30 }}>Recent Catches</h3>
          <ul>
            {catches.map((c) => (
              <li key={c.id}>
                🐟 <b>{c.species}</b> ×{c.quantity} at ({c.lat}, {c.lon})
              </li>
            ))}
          </ul>
        </div>

        {/* ----------- Right Section: Hotspots ----------- */}
        <div style={{ flex: 1 }}>
          <h3>Predicted Hotspots</h3>
          {hotspots.length > 0 ? (
            <ul>
              {hotspots.map((h, i) => (
                <li key={i}>
                  🌊 <b>{h.species}</b> — ({h.lat.toFixed(3)}, {h.lon.toFixed(3)}) — Probability: {Math.round(h.prob * 100)}%
                </li>
              ))}
            </ul>
          ) : (
            <p>No predictions yet. Log a few catches first!</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
