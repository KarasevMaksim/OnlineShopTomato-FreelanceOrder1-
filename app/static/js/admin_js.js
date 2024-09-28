document.addEventListener('DOMContentLoaded', function() {
    var selectSection = document.getElementById('select_section');

    selectSection.addEventListener('change', function() {
        var sectionName = this.value;
        fetch('get_sub_sections', {
            method: 'POST',
            body: JSON.stringify({ section: sectionName }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ form.hidden_tag() }}'
            }
        })
        .then(response => response.json())
        .then(data => {
            var selectSubSection = document.getElementById('select_sub_section');
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