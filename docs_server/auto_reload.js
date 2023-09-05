
(() => {
    let lastUUID = null;
    let lastUpdateTime = null;
    async function checkForUpdates(firstTime) {
        let options = { method: 'HEAD', cache: firstTime ? "force-cache" : "reload", mode: "same-origin" };
        let headers = (await fetch(location.href, options)).headers;
        let uuid = '' + headers.get('eTag') + ';' + headers.get('Last-Modified');
        if (lastUUID !== null && uuid !== lastUUID) {
            div = document.createElement('div');
            div.innerHTML = `<div id="_reloadingPopup" style="position: fixed; top: 20px; left: 20px;
                z-index: 10001; background-color: #800; color: white; font-weight: bold; font-size: 300%;
                padding: 40px; box-shadow: 0 0 20px #800;">Page reloading...</div>`;
            document.body.appendChild(div);
            setTimeout(() => location.reload(), 500);
        }
        lastUUID = uuid;
    }
    async function animationFrame(time) {
        try {
            if (lastUpdateTime === null || time - lastUpdateTime > 1000) {
                lastUpdateTime = time;
                await checkForUpdates(time == null);
            }
        } finally {
            setTimeout(() => window.requestAnimationFrame(animationFrame), 1000);
        }
    }
    animationFrame(null);
})();

let autoReloadPopupIter = null;

function autoReloadPopup(time) {
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
        autoReloadPopupIter = time + 3000;
    } else {
        div = document.getElementById('_autoReloadPopup');
    }
    let delta = (autoReloadPopupIter - time) / 10
    console.log(delta);
    div.style.opacity = Math.min(100, delta) + '%';
    if (delta > 100) {
        setTimeout(() => window.requestAnimationFrame(autoReloadPopup), (delta - 100) * 10);
    } else if (delta >= 0) {
        window.requestAnimationFrame(autoReloadPopup);
    } else {
            div.style.display = 'none';
    }
}

window.addEventListener('DOMContentLoaded', () => window.requestAnimationFrame(autoReloadPopup));
