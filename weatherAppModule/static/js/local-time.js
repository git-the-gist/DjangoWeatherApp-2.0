
let time = document.getElementById("time-txt");
let isTrue = document.getElementById("isFahrenheit");

const displayLocalTime = (format) => { // display user local time
    let date = new Date();
    let options = {
        hour: '2-digit', 
        minute: '2-digit'
    };

    return date.toLocaleString(format, options);
}

const changeFormat = () => { // change format of time
    let format = isFahrenheit ? 'en-GB' : 'en-US';
    time.textContent = displayLocalTime(format);
}

setInterval(changeFormat, 10)

setInterval(displayLocalTime, 1000);




