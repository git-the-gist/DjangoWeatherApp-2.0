
document.addEventListener('DOMContentLoaded', () => { // autocomplete search bar
    const searchInput = document.getElementById('search');
    const suggestionsContainer = document.getElementById('suggestions');
    const suggestionsList = document.getElementById('suggestions-list');

    searchInput.addEventListener('input', function () {
        const query = this.value.trim();

        if (query.length > 0) {
            fetchSuggestions(query);
        } else {
            clearSuggestions();
        }
    });

    function fetchSuggestions(query) { // fetch search suggestions from API
        const apiUrl = `http://127.0.0.1:8000/weathersource/api/search?city=${encodeURIComponent(query)}`;
        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                displaySuggestions(data.data.slice(0, 100));
            })
            .catch(error => {
                console.error('Error fetching suggestions:', error);
            });
    }

    function displaySuggestions(suggestions) { // display search suggestions
        clearSuggestions();
        if (searchInput.value !== '') {
            suggestions.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item.suggestion;

                li.addEventListener('mouseover', () => {
                    li.style.backgroundColor = '#127784';
                });

                li.addEventListener('mouseout', () => {
                    li.style.backgroundColor = '';
                });

                li.addEventListener('click', function () {
                    performSearch(item.suggestion);
                });

                suggestionsList.appendChild(li);
            });
            suggestionsContainer.style.display = 'block';
        }
    }

    function clearSuggestions() { // clear search suggestions
        suggestionsList.innerHTML = '';
        suggestionsContainer.style.display = 'none';
    }

    function performSearch(selectedCity) { //perform search and redirect to search results

        const basePath = '/weathersource/search';
        const url = `${basePath}?city=${encodeURIComponent(selectedCity)}`;
    
        try {
            window.location.assign(url);
        } catch (error) {
            console.error('Navigation error:', error);
        }

        searchInput.value = '';
        clearSuggestions();
    }

    searchInput.addEventListener('keydown', function (event) { // Prevent manual submission of input (pressing Enter)
        if (event.key === 'Enter') {
            event.preventDefault();
        }
    });
});
