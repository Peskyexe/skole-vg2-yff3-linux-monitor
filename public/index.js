function sleep(ms) {
    return new Promise(reslove => setTimeout(reslove, ms))
}

async function getSystemData() {
    try {
        const response = await fetch('../shared/systemdata.json');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(error)
    }
}

async function updateDashboard() {
    const systemData = await getSystemData();

    // HTML-en er satt opp sånn at elementene som skal bli endret sin ID er det samme som nøkkelen i systemData til verdien den skal bli endret til
    
    // Går gjennom hver nøkkel og verdi par fra input objektet og oppdatere DOM-en med de.
    const updateDOMwithObject = (object) => {
        for (const [key, value] of Object.entries(object)) {
            try {
                const el = document.getElementById(key);
                el.textContent = value;
            } catch (error) {
                console.error(error);
            }
        }
    }

    const updateRadialBar = (radialBarId, newValue) => {
        try {
            // Sikkrer at verdien ikke er mer 100 eller mindre en 0
            const boundedValue = Math.min(Math.max(newValue, 0), 100);
            const el = document.getElementById(radialBarId);

            el.style.setProperty('--progress', boundedValue);
        } catch (error) {
            console.error(error)
        }
    }

    updateDOMwithObject(systemData['system_info']);

    // Prossesor 
    updateDOMwithObject(systemData['cpu']);
    updateRadialBar('cpu-radial-bar', systemData['cpu']['cpu_used_percent']);

    // RAM
    updateDOMwithObject(systemData['memory']);
    updateRadialBar('memory-radial-bar', systemData['memory']['memory_used_percent']);

    // Lagring
    updateDOMwithObject(systemData['disk']);
    updateRadialBar('disk-radial-bar', systemData['disk']['disk_used_percent']);
}


// Henter in system data og oppdater DOM
// Så venter 2 sekunder før den looper igjen
async function updateLoop() {
    while (true) {
        await updateDashboard();
        await sleep(2000)
    }
}

updateLoop();