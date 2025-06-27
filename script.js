const moodPills = document.querySelectorAll("#moodPills .pill");
const langPills = document.querySelectorAll("#langPills .pill");
const submitBtn = document.getElementById("submitBtn");
const artistInput = document.getElementById("artistInput");
const statusDiv = document.getElementById("status");

let selectedMood = "";
let selectedLang = "";

// Handle pill selection
moodPills.forEach(pill => {
  pill.addEventListener("click", () => {
    moodPills.forEach(p => p.classList.remove("selected"));
    pill.classList.add("selected");
    selectedMood = pill.innerText.toLowerCase();
  });
});

langPills.forEach(pill => {
  pill.addEventListener("click", () => {
    langPills.forEach(p => p.classList.remove("selected"));
    pill.classList.add("selected");
    selectedLang = pill.innerText.toLowerCase();
  });
});

// Handle submit
submitBtn.addEventListener("click", () => {
  const artist = artistInput.value;

  if (!selectedMood || !selectedLang) {
    statusDiv.innerHTML = "❌ Please select both mood and language.";
    return;
  }

  fetch("https://moodify-backend-953666257830.asia-south1.run.app/recommend", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      mood: selectedMood,
      language: selectedLang,
      artist: artist
    })
  })
  .then(res => res.json())
  .then(data => {
    if (data.status === "success") {
      statusDiv.innerHTML = "✅ Playlist generated!";
      document.getElementById("preview").innerHTML = `
        <p><a href="${data.playlist_url}" target="_blank" style="color:#1db954;font-weight:bold;">🎧 Open Playlist on Spotify</a></p>
      `;
    } else {
      statusDiv.innerHTML = "❌ Failed to get playlist.";
    }
  })
  .catch(err => {
    console.error(err);
    statusDiv.innerHTML = "❌ Failed to reach server.";
  });
});
