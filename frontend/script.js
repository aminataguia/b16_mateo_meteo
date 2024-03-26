function sendCitySelection() {
    var city = document.getElementById("citySelect").value;
    if (city) {
        // Replace 'your_api_endpoint' with the actual endpoint of your API
        var apiUrl = 'your_api_endpoint/' + city;
        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                // Handle the response data from your API
                console.log(data);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }
}

