document.addEventListener('DOMContentLoaded', function() {
    const pokemonInput = document.querySelector('input[name="name"]');
    const dropdown = document.createElement('div');
    dropdown.className = 'pokemon-dropdown';
    pokemonInput.parentElement.classList.add('input-container');
    pokemonInput.parentElement.appendChild(dropdown);

    let selectedIndex = -1;
    let filteredPokemon = [];

    function filterPokemon(input) {
        const value = input.toLowerCase();
        const matches = window.pokemonNames.filter(name => name.includes(value));
        
        // Sort matches to prioritize prefix matches
        return matches.sort((a, b) => {
            const aStartsWith = a.toLowerCase().startsWith(value);
            const bStartsWith = b.toLowerCase().startsWith(value);
            
            if (aStartsWith && !bStartsWith) return -1;
            if (!aStartsWith && bStartsWith) return 1;
            return a.localeCompare(b); // If both are prefix matches or both aren't, sort alphabetically
        });
    }

    function showDropdown(filteredPokemon) {
        dropdown.innerHTML = '';
        if (filteredPokemon.length === 0) {
            dropdown.classList.remove('show');
            return;
        }
        
        filteredPokemon.forEach((name, index) => {
            const option = document.createElement('div');
            option.className = 'pokemon-option';
            option.textContent = name;
            option.addEventListener('click', () => {
                pokemonInput.value = name;
                dropdown.classList.remove('show');
                selectedIndex = -1;
                pokemonInput.form.submit();
            });
            dropdown.appendChild(option);
        });
        dropdown.classList.add('show');
    }

    function updateSelectedOption() {
        const options = dropdown.getElementsByClassName('pokemon-option');
        for (let i = 0; i < options.length; i++) {
            options[i].classList.remove('selected');
        }
        if (selectedIndex >= 0 && selectedIndex < options.length) {
            options[selectedIndex].classList.add('selected');
            options[selectedIndex].scrollIntoView({ block: 'nearest' });
        }
    }

    pokemonInput.addEventListener('input', (e) => {
        const value = e.target.value;
        if (value.length > 0) {
            filteredPokemon = filterPokemon(value);
            showDropdown(filteredPokemon);
            selectedIndex = -1;
        } else {
            dropdown.classList.remove('show');
            selectedIndex = -1;
        }
    });

    pokemonInput.addEventListener('keydown', (e) => {
        if (!dropdown.classList.contains('show')) return;

        const options = dropdown.getElementsByClassName('pokemon-option');
        
        switch(e.key) {
            case 'ArrowDown':
                e.preventDefault();
                selectedIndex = Math.min(selectedIndex + 1, options.length - 1);
                updateSelectedOption();
                break;
            case 'ArrowUp':
                e.preventDefault();
                selectedIndex = Math.max(selectedIndex - 1, 0);
                updateSelectedOption();
                break;
            case 'Enter':
                e.preventDefault();
                if (selectedIndex >= 0 && selectedIndex < options.length) {
                    pokemonInput.value = options[selectedIndex].textContent;
                    dropdown.classList.remove('show');
                    selectedIndex = -1;
                    pokemonInput.form.submit();
                }
                break;
            case 'Escape':
                e.preventDefault();
                dropdown.classList.remove('show');
                selectedIndex = -1;
                break;
        }
    });

    document.addEventListener('click', (e) => {
        if (!pokemonInput.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.classList.remove('show');
            selectedIndex = -1;
        }
    });
}); 