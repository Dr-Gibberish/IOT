async function fetchMoistureLevels() {
    try {
        const response = await fetch('http://172.31.85.34:5002/moisture');
        const data = await response.json();
        const moistureLevels = data.moisture;
        const timeStamp = data.timer_read;

        const container = document.getElementById('moisture-levels');
        container.innerHTML = '';
        container.classList.add('border-2')

        moistureLevels.forEach((level, index) => {
            const div = document.createElement('div');
            div.textContent = `${index+1}  |  ${timeStamp[index]}  |  ${level.toFixed(2)}`;
            container.appendChild(div);
            div.classList.add('border-2')
        });
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

let previousMoistureStatus = null; 
async function fetchPumpStatus() {
    try{
        const response2 = await fetch('http://172.31.85.34:5002/pumpstatus');
        const data2 = await response2.json();
        const pumpStatus = data2.pump_status;

        if( pumpStatus !== previousMoistureStatus) {
            const container2 = document.getElementById('pump-status');
            container2.innerHTML = '';
            const statusDiv = document.createElement('div');
            statusDiv.textContent = `Pump Status: ${pumpStatus ? 'On' : 'Off'}`;
            container2.appendChild(statusDiv);

            previousMoistureStatus = pumpStatus;
        }
    } catch (error){
        console.log("Error fetching data:", error);
    }
}

window.onload = function() {
    fetchMoistureLevels();
    setInterval(fetchMoistureLevels, 5000);
    fetchPumpStatus();
    setInterval(fetchPumpStatus,5000);
};
