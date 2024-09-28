document.addEventListener('DOMContentLoaded', function() {
    var selectSection = document.getElementById('select_section2');

    selectSection.addEventListener('change', function() {
        var sectionName = this.value;
        fetch('product-filter', {
            method: 'POST',
            body: JSON.stringify({ section2: sectionName }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ form2.hidden_tag() }}'
            }
        })
        .then(response => response.json())
        .then(data => {
            var selectSubSection = document.getElementById('select_sub_section2');
            selectSubSection.innerHTML = '';
            data.sub_sections.forEach(function(subSection) {
                var option = document.createElement('option');
                option.value = subSection[0];
                option.textContent = subSection[1];
                selectSubSection.appendChild(option);
            });
        })
        .catch(function(error) {
            console.error('Error:', error);
        });
    });
});