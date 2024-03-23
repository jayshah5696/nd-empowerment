chrome.contextMenus.create({
  title: "Explain",
  contexts: ["selection"],
  onclick: processTextWithAPI.bind(null, "http://127.0.0.1:8000/explain")
});

chrome.contextMenus.create({
  title: "Read",
  contexts: ["selection"],
  onclick: processTextWithAPI.bind(null, "http://127.0.0.1:8000/read")
});

chrome.contextMenus.create({
  title: "Visualize",
  contexts: ["selection"],
  onclick: processTextWithAPI.bind(null, "http://127.0.0.1:8000/visualize")
});


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
    .then(processedData => {
      if (apiUrl === "http://127.0.0.1:8000/visualize") {
        // Open the image in a new tab
        chrome.tabs.create({ url: `file:///${processedData}` });
      } else {
        // Open the processed text in a new tab
        chrome.tabs.create({ url: `data:text/html,<pre>${processedData}</pre>` });
      }
    })
    .catch(error => {
      console.error('Error:', error);
      // Handle error cases
    });
}
