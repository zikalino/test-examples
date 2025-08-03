chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    chrome.scripting.executeScript({
    target : {tabId : request['tab-id']},
        func : (elementId, value) => {
            document.getElementById(elementId).value = value
        },
    args : [ request['element-id'], request['value']],
    });
    //sendResponse("OK");
  }
);


chrome.offscreen.createDocument({
  url: 'offscreen.html',
  reasons: ['CLIPBOARD'],
  justification: 'reason for needing the document',
});
