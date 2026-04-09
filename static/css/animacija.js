function startSneg() {
    const overlay = document.getElementById("Animacija");

    /*Снегулка*/
    const snegInterval = setInterval(() => {
        const el = document.createElement("div");
        el.classList.add("snegulka");
        el.innerHTML = "❄"; 

        el.style.left = Math.random() * 100 + "vw";
        el.style.fontSize = (10 + Math.random() * 15) + "px";
        el.style.animationDuration = (4 + Math.random() * 4) + "s";

        overlay.appendChild(el);

        setTimeout(() => el.remove(), 9000);
    }, 150);

    setTimeout(() => clearInterval(snegInterval), 15000);
}
startSneg();

/*Огномет*/
function startOgnometi() {
    const overlay = document.getElementById("Animacija");

    const boi = ["red", "yellow", "cyan", "lime", "orange", "magenta", "blue", "violet", "gold", "white"];

    const ognInterval = setInterval(() => {
        const x = Math.random() * window.innerWidth;
        const y = Math.random() * window.innerHeight * 0.5;

        for (let i = 0; i < 30; i++) {
            const p = document.createElement("div");
            p.classList.add("cestica");

            const agol = Math.random() * Math.PI * 2;
            const dist = 80 + Math.random() * 60;

            p.style.left = x + "px";
            p.style.top = y + "px";

            p.style.background = boi[Math.floor(Math.random() * boi.length)];

            p.style.setProperty("--dx", Math.cos(agol) * dist + "px");
            p.style.setProperty("--dy", Math.sin(agol) * dist + "px");

            overlay.appendChild(p);

            setTimeout(() => p.remove(), 1200);
        }
    }, 350);

    setTimeout(() => clearInterval(ognInterval), 15000);
}

startOgnometi();
