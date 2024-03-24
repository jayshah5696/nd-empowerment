chrome.contextMenus.create({
  title: "EXPLAIN",
  contexts: ["selection"],
  onclick: processTextWithAPI.bind(null, "http://127.0.0.1:8000/explain")
});

chrome.contextMenus.create({
  title: "READ",
  contexts: ["selection"],
  onclick: readText
});

chrome.contextMenus.create({
  title: "VISUALIZE",
  contexts: ["selection"],
  onclick: visualizeText
});

function visualizeText(info) {
  const selectedText = info.selectionText;
  const apiUrl = "http://127.0.0.1:8000/visualize";
  processTextWithAPI(apiUrl, info);
}

// Function to process text with API
function processTextWithAPI(apiUrl, info) {
  const selectedText = info.selectionText;
  const requestPayload = { text: selectedText };

  fetch(apiUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestPayload)
  })
  .then(response => response.text())
  .then(imageUrl => {
    console.log('Image URL:', imageUrl);

    // Open popup window with the image URL when the user clicks on the context menu item
    chrome.windows.create({
      url: imageUrl,
      type: 'popup',
      width: 400,
      height: 300
    });
  })
  .catch(error => {
    console.error('Error:', error);
    // Handle error cases
  });
}

function readText(info) {
  const selectedText = info.selectionText;

  // Assuming the API returns the local path to the .wav file
  fetch(`http://127.0.0.1:8000/read?text=${encodeURIComponent(selectedText)}`)
    .then(response => response.text())
    .then(wavFilePath => {
      const audio = new Audio(`file:///${wavFilePath}`);
      audio.play();
    })
    .catch(error => {
      console.error('Error:', error);
      // Handle error cases
    });
}
