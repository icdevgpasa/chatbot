

document.addEventListener("DOMContentLoaded", function (event) {


    chrome.storage.local.get(['kid', 'fight', 'help'], function (result) {
        document.querySelector('#kid').checked = result.kid;
        document.querySelector('#fight').checked = result.fight;
        document.querySelector('#help').checked = result.help
        result.kid ? document.querySelector('#imgkid').classList.remove('off') : document.querySelector('#imgkid').classList.add('off');
        result.fight ? document.querySelector('#imgviki').classList.remove('off') : document.querySelector('#imgviki').classList.add('off');
    });

    document.querySelector('#kid').addEventListener('change', function () {
        chrome.storage.local.set({ 'kid': this.checked });
        if (this.checked) {
            document.querySelector('#fight').checked = false;
            chrome.storage.local.set({ 'fight': false });
            document.querySelector('#imgkid').classList.remove('off');
            document.querySelector('#imgviki').classList.add('off');
            
        } else {
            document.querySelector('#fight').checked = true;
            chrome.storage.local.set({ 'fight': true });
            document.querySelector('#imgkid').classList.add('off');
            document.querySelector('#imgviki').classList.remove('off');
        }
        
        sendToCore();
    });
    document.querySelector('#fight').addEventListener('change', function () {
        chrome.storage.local.set({ 'fight': this.checked });
        if (this.checked) {
            document.querySelector('#kid').checked = false;
            chrome.storage.local.set({ 'kid': false });
            document.querySelector('#imgkid').classList.add('off');
            document.querySelector('#imgviki').classList.remove('off');
        } else {
            document.querySelector('#kid').checked = true;
            chrome.storage.local.set({ 'kid': true });
            document.querySelector('#imgkid').classList.remove('off');
            document.querySelector('#imgviki').classList.add('off');
        }
        sendToCore();

    });
    document.querySelector('#help').addEventListener('change', function () {
        chrome.storage.local.set({ 'help': this.checked });
        sendToCore();
    });
  
    
});

function sendToCore() {
    chrome.runtime.sendMessage({settings: 'update', kid: document.querySelector('#kid').checked, fight: document.querySelector('#fight').checked, help: document.querySelector('#help').checked },
        function (response) {

        });
}