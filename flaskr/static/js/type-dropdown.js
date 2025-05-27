document.addEventListener('DOMContentLoaded', function() {
    const types = [
        'normal', 'fire', 'water', 'electric', 'grass', 'ice',
        'fighting', 'poison', 'ground', 'flying', 'psychic',
        'bug', 'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy'
    ];

    createDropdown({
        inputSelector: 'input[name="name"]',
        dropdownClass: 'type-dropdown',
        optionClass: 'type-option',
        filterFunction: (value) => types.filter(type => 
            type.toLowerCase().includes(value.toLowerCase())
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
        dataSource: types
    });
}); 