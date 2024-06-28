function sendUrl() {
    (async () => {
        const [tab] = await chrome.tabs.query({active: true, lastFocusedWindow: true});
        const url = tab.url;
        fetch('http://localhost:5000/receive_url', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: url })
        });
      })();
}

sendUrl();
setInterval(sendUrl, 500); // Send the URL every 0.5 secs
