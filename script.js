let selectedMood = "";
let selectedLang = "";

document.querySelectorAll('#mood-pills .pill').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('#mood-pills .pill').forEach(b => b.classList.remove('selected'));
    btn.classList.add('selected');
    selectedMood = btn.dataset.value;
  });
});

document.querySelectorAll('#lang-pills .pill').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('#lang-pills .pill').forEach(b => b.classList.remove('selected'));
    btn.classList.add('selected');
    selectedLang = btn.dataset.value;
  });
});

document.getElementById('moodForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const artist = document.getElementById('artist').value;
  const statusDiv = document.getElementById('status');
  statusDiv.textContent = "⏳ Sending your mood...";

  if (!selectedMood || !selectedLang) {
    statusDiv.textContent = "⚠️ Please select both mood and language.";
    return;
  }

  try {
    const response = await fetch("https://moodify-backend-953666257830.asia-south1.run.app/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        mood: selectedMood,
        language: selectedLang,
        artist: artist
      })
    });

    const data = await response.json();

    if (response.ok) {
      statusDiv.innerHTML = `✅ Playlist generated successfully!<br><small>Message ID: ${data.message_id}</small>`;
    } else {
      statusDiv.textContent = `❌ Error: ${data.error || "Unknown error"}`;
    }
  } catch (err) {
    statusDiv.textContent = "❌ Failed to reach server.";
  }
});
