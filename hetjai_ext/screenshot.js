function setScreenshotUrl(url,pageUrl) {
    document.getElementById('pageUrl').innerText =pageUrl;
    var data = new Date();
    document.getElementById('data').innerText = 'Data: '+data.toLocaleDateString()+" "+data.toLocaleTimeString();
    document.getElementById('target').src = url;
  }
  function showInfo() {
      alert('ToDo :)');
  }