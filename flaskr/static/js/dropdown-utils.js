/**
 * Creates and manages a dropdown with filtering and keyboard navigation.
 * @param {Object} config Configuration object for the dropdown
 * @param {string} config.inputSelector CSS selector for the input element
 * @param {string} config.dropdownClass CSS class for the dropdown container
 * @param {string} config.optionClass CSS class for dropdown options
 * @param {Function} config.filterFunction Function to filter items based on input
 * @param {Array} config.dataSource Array of items to populate the dropdown
 * @param {Function} [config.sortFunction] Optional function to sort filtered items
 */
function createDropdown(config) {
    const {
        inputSelector,
        dropdownClass,
        optionClass,
        filterFunction,
        dataSource,
        sortFunction
    } = config;

    const input = document.querySelector(inputSelector);
    const dropdown = document.createElement('div');
    dropdown.className = dropdownClass;
    input.parentElement.classList.add('input-container');
    input.parentElement.appendChild(dropdown);

    let selectedIndex = -1;
    let filteredItems = [];

    function showDropdown(filteredItems) {
        dropdown.innerHTML = '';
        if (filteredItems.length === 0) {
            dropdown.classList.remove('show');
            return;
        }
        
        filteredItems.forEach((item, index) => {
            const option = document.createElement('div');
            option.className = optionClass;
            option.textContent = item;
            option.addEventListener('click', () => {
                input.value = item;
                dropdown.classList.remove('show');
                selectedIndex = -1;
                input.form.submit();
            });
            dropdown.appendChild(option);
        });
        dropdown.classList.add('show');
    }

    function updateSelectedOption() {
        const options = dropdown.getElementsByClassName(optionClass);
        for (let i = 0; i < options.length; i++) {
            options[i].classList.remove('selected');
        }
        if (selectedIndex >= 0 && selectedIndex < options.length) {
            options[selectedIndex].classList.add('selected');
            options[selectedIndex].scrollIntoView({ block: 'nearest' });
        }
    }

    input.addEventListener('input', (e) => {
        const value = e.target.value;
        if (value.length > 0) {
            filteredItems = filterFunction(value);
            if (sortFunction) {
                filteredItems = sortFunction(filteredItems, value);
            }
            showDropdown(filteredItems);
            selectedIndex = -1;
        } else {
            dropdown.classList.remove('show');
            selectedIndex = -1;
        }
    });

    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && input.value.trim()) {
            e.preventDefault();
            input.form.submit();
            return;
        }

        if (!dropdown.classList.contains('show')) return;

        const options = dropdown.getElementsByClassName(optionClass);
        
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
                    input.value = options[selectedIndex].textContent;
                    dropdown.classList.remove('show');
                    selectedIndex = -1;
                    input.form.submit();
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
        if (!input.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.classList.remove('show');
            selectedIndex = -1;
        }
    });
} 