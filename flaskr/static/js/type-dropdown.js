document.addEventListener('DOMContentLoaded', function() {
    const typeInput = document.querySelector('input[name="name"]');
    const dropdown = document.createElement('div');
    dropdown.className = 'type-dropdown';
    typeInput.parentElement.classList.add('input-container');
    typeInput.parentElement.appendChild(dropdown);

    const types = [
        'normal', 'fire', 'water', 'electric', 'grass', 'ice',
        'fighting', 'poison', 'ground', 'flying', 'psychic',
        'bug', 'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy'
    ];

    let selectedIndex = -1;
    let filteredTypes = [];

    function filterTypes(input) {
        const value = input.toLowerCase();
        return types.filter(type => type.includes(value));
    }

    function showDropdown(filteredTypes) {
        dropdown.innerHTML = '';
        filteredTypes.forEach((type, index) => {
            const option = document.createElement('div');
            option.className = 'type-option';
            option.textContent = type;
            option.addEventListener('click', () => {
                typeInput.value = type;
                dropdown.classList.remove('show');
                selectedIndex = -1;
            });
            dropdown.appendChild(option);
        });
        dropdown.classList.add('show');
    }

    function updateSelectedOption() {
        const options = dropdown.getElementsByClassName('type-option');
        for (let i = 0; i < options.length; i++) {
            options[i].classList.remove('selected');
        }
        if (selectedIndex >= 0 && selectedIndex < options.length) {
            options[selectedIndex].classList.add('selected');
            options[selectedIndex].scrollIntoView({ block: 'nearest' });
        }
    }

    typeInput.addEventListener('input', (e) => {
        const value = e.target.value;
        if (value.length > 0) {
            filteredTypes = filterTypes(value);
            showDropdown(filteredTypes);
            selectedIndex = -1;
        } else {
            dropdown.classList.remove('show');
            selectedIndex = -1;
        }
    });

    typeInput.addEventListener('keydown', (e) => {
        if (!dropdown.classList.contains('show')) return;

        const options = dropdown.getElementsByClassName('type-option');
        
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
                    typeInput.value = options[selectedIndex].textContent;
                    dropdown.classList.remove('show');
                    selectedIndex = -1;
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
        if (!typeInput.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.classList.remove('show');
            selectedIndex = -1;
        }
    });
}); 