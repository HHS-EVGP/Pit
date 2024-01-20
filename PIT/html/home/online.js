// import fs from 'fs';

let secondsWebsite = 0;
let secondsCollect = 0;
let secondsSend = 0;
let timeTillCheck = 0;

let wasOnlineCollect = false;
let wasOnlineSend = false;

async function updateTime() {timeTillCheck

    document.getElementById("timeTillCheck").innerHTML = timeTillCheck;

    document.getElementById("websiteLastUpdated").innerHTML = "Lasted Updated: " + secondsWebsite.toString() + " seconds ago";
    document.getElementById("dataCollectionLastUpdated").innerHTML = "Lasted Updated: " + secondsCollect.toString() + " seconds ago";
    document.getElementById("dataSendLastUpdated").innerHTML = "Lasted Updated: " + secondsSend.toString() + " seconds ago";
    secondsWebsite++;
    secondsCollect++;
    secondsSend++;
    

    timeTillCheck--;
    if(timeTillCheck == -1){
        timeTillCheck = 5
        //DO THE CHECK!!!
    
        const recive = await isReciveOnline();
        if(recive){
            wasOnlineCollect = true;
        }else{
            wasOnlineCollect = false;
        }

        
    
        wasOnlineSend = true;
        wasOnlineSend = false;
    }


    updateOnlineStatus(0,wasOnlineCollect);
    updateOnlineStatus(1,wasOnlineSend);
    

}

function pausecomp(millis)
{
    var date = new Date();
    var curDate = null;
    do { curDate = new Date(); }
    while(curDate-date < millis);
}

async function isReciveOnline(){
    const newestFile = await findNewestFile();
    console.log(newestFile);
    const first = await getNewestDataPoints(newestFile);
    pausecomp(500)
    const second = await getNewestDataPoints(newestFile);

    if (second == first){
        return false
    }else{
        return true
    }
}

async function getNewestDataPoints(csvFilePath) {
  try {
    // Fetch the CSV file
    const response = await fetch(csvFilePath);
    const csvData = await response.text();

    // Parse CSV data using Papaparse
    const parsedData = Papa.parse(csvData, { header: true });

    // Get the newest 10 data points
    const newestDataPoints = parsedData.data.slice(-2);

    // Log or use the newest data points as needed
    // console.log(newestDataPoints[0]["counter"]);
    return newestDataPoints[0]["counter"];

    // Return the newest data points
    return newestDataPoints;
  } catch (error) {
    console.error('Error fetching or parsing CSV file:', error);
    return null;
  }
}

async function findNewestFile() {
    let name = "none";

    const checkFileExistence = async (filePath) => {
        try {
            const response = await fetch(filePath, { method: 'HEAD' });
            return response.ok;
        } catch (error) {
            return false;
        }
    };

    let index = 0;

    const findNonExistingIndex = async () => {
        while (await checkFileExistence(`/2024/${index}.data.csv`)) {
            index++;
        }
        return index;
    };

    const result = await findNonExistingIndex();
    const newFileName = `/2024/${result-1}.data.csv`;
    return newFileName;
}
function updateOnlineStatus(picker,choice) {
    const websiteStatus = document.getElementById('websiteStatus');
    const dataCollectionStatus = document.getElementById('dataCollectionStatus');
    const dataSendStatus = document.getElementById('dataSendStatus');


    websiteStatus.textContent = 'ONLINE';
    websiteStatus.classList.remove('offline');
    websiteStatus.classList.add('online');
    

    if (picker == 0){
        if (choice) {
            if(dataCollectionStatus.textContent == 'OFFLINE'){
                secondsCollect = 0;
            }
            dataCollectionStatus.textContent = 'ONLINE';
            dataCollectionStatus.classList.remove('offline');
            dataCollectionStatus.classList.add('online');
        } else {
            if(dataCollectionStatus.textContent == 'ONLINE'){
                secondsCollect = 0;
            }
            dataCollectionStatus.textContent = 'OFFLINE';
            dataCollectionStatus.classList.remove('online');
            dataCollectionStatus.classList.add('offline');
        }
    }else{
        if (choice) {
            if(dataSendStatus.textContent == 'OFFLINE'){
                secondsSend = 0;
            }
            dataSendStatus.textContent = 'ONLINE';
            dataSendStatus.classList.remove('offline');
            dataSendStatus.classList.add('online');
        } else {
            if(dataSendStatus.textContent == 'ONLINE'){
                secondsSend = 0;
            }
            dataSendStatus.textContent = 'OFFLINE';
            dataSendStatus.classList.remove('online');
            dataSendStatus.classList.add('offline');
        }
    }

    
}

setInterval(updateTime, 1000);