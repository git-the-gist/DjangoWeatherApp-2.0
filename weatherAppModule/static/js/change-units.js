
    const DOMContainer = {
        wind: document.getElementsByClassName('wind-value')[0],
        temp: document.getElementsByClassName('temp-txt')[0],
        high: document.getElementsByClassName('high-value')[0],
        low: document.getElementsByClassName('low-value')[0],
        sunrise: document.getElementsByClassName('sunrise-value')[0],
        sunset: document.getElementsByClassName('sunset-value')[0],
        unit: document.getElementsByClassName('unit'),
        button: document.getElementById('toggle-button'),
    };



    let isFahrenheit = true;

    function updateWeatherData(unit) { // update weather data
        DOMContainer.wind.textContent = `${weatherData[unit].wind}${unit === 'fahrenheit' ? 'mph' : 'km/h'}`;
        DOMContainer.temp.textContent = `${weatherData[unit].temp}\u00B0${unit === 'fahrenheit' ? 'F' : 'C'}`;
        DOMContainer.high.textContent = `${weatherData[unit].high}\u00B0`;
        DOMContainer.low.textContent = `${weatherData[unit].low}\u00B0`;
        DOMContainer.sunrise.textContent = weatherData[unit].sunrise;
        DOMContainer.sunset.textContent = weatherData[unit].sunset;
    }

    function toggleData() { // toggle between Fahrenheit and Celsius
        const unit = isFahrenheit ? 'fahrenheit' : 'celsius';
        updateWeatherData(unit);
        DOMContainer.button.textContent = isFahrenheit ? "\u00B0C" : "\u00B0F";
        isFahrenheit = !isFahrenheit;
    }


    updateWeatherData('celsius'); // set initial data to Celsius
    DOMContainer.button.textContent = "\u00B0F";

    DOMContainer.button.addEventListener('click', toggleData); // add event listener to toggle button