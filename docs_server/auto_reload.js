
let autoReloadDate = null;

async function checkReload() {
    try {
        let response = await fetch('/lastBuild.txt', { cache: 'no-store' });
        if (response.status == 200) {
            let date = await response.text();
            if (autoReloadDate === null || autoReloadDate == date) {
                autoReloadDate = date;
            } else {
                location.reload();
            }
        } else {
            console.warn(`Cannot get '/lastBuild.txt', status ${response.status}`);
        }
    } catch (ex) {
        console.warn(`Cannot get '/lastBuild.txt',`, ex);
    } finally {
        setTimeout(checkReload, 1000);
    }
}

let autoReloadPopupIter = null;

function autoReloadPopup() {
    let pageAccessedByReload = (
        (window.performance.navigation && window.performance.navigation.type === 1) ||
        window.performance
            .getEntriesByType('navigation')
            .map((nav) => nav.type)
            .includes('reload')
    );
    if (!pageAccessedByReload) {
        return;
    }
    let div;
    if (autoReloadPopupIter === null) {
        div = document.createElement('div');
        div.innerHTML = `<div id="_autoReloadPopup" style="position: fixed; top: 20px; left: 20px;
            z-index: 10000; background-color: #080; color: white; font-weight: bold; font-size: 300%;
            padding: 40px; box-shadow: 0 0 20px #080;">Page reloaded</div>`;
        document.body.appendChild(div);
        autoReloadPopupIter = 300;
    } else {
        div = document.getElementById('_autoReloadPopup');
    }
    div.style.opacity = Math.min(100, autoReloadPopupIter) + '%';
    autoReloadPopupIter -= 5;
    if (autoReloadPopupIter >= 0) {
        setTimeout(autoReloadPopup, 50);
    } else {
        div.style.display = 'none';
    }
}

setTimeout(checkReload, 1);
window.addEventListener('DOMContentLoaded', autoReloadPopup);