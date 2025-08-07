let prevURL = "";

function sendUrl() {
    (async () => {
        const [tab] = await chrome.tabs.query({active: true, lastFocusedWindow: true});
        const url = tab.url;
        if (url != prevURL) {
            prevURL = url;
            fetch('http://localhost:5000/update_url', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url: url })
            });
        }
      })();
}

sendUrl();
setInterval(sendUrl, 300); // Send the URL every 0.3 secs
