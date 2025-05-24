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
        dataSource: types
    });
}); 