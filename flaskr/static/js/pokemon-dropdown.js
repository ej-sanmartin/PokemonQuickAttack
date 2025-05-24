document.addEventListener('DOMContentLoaded', function() {
    createDropdown({
        inputSelector: 'input[name="name"]',
        dropdownClass: 'pokemon-dropdown',
        optionClass: 'pokemon-option',
        filterFunction: (value) => window.pokemonNames.filter(name => 
            name.toLowerCase().includes(value.toLowerCase())
        ),
        sortFunction: (matches, value) => {
            return matches.sort((a, b) => {
                const aStartsWith = a.toLowerCase().startsWith(value.toLowerCase());
                const bStartsWith = b.toLowerCase().startsWith(value.toLowerCase());
                
                if (aStartsWith && !bStartsWith) return -1;
                if (!aStartsWith && bStartsWith) return 1;
                return a.localeCompare(b);
            });
        },
        dataSource: window.pokemonNames
    });
}); 