$(document).ready(function () {
    const BASE_URL = '/api/cupcakes';

    // Function to generate cupcake HTML
    function generateCupcakeHTML(cupcake) {
        return `
            <li class="list-group-item">
                <img src="${cupcake.image}" alt="${cupcake.flavor}" style="width:50px; height:50px;">
                ${cupcake.flavor} - ${cupcake.size} - ${cupcake.rating}/10
            </li>
        `;
    }

    // Function to fetch and display cupcakes
    async function loadCupcakes() {
        const response = await axios.get(BASE_URL);
        for (let cupcake of response.data.cupcakes) {
            $('#cupcakes-list').append(generateCupcakeHTML(cupcake));
        }
    }

    // Load cupcakes on page load
    loadCupcakes();

    // Handle form submission for adding a new cupcake
    $('#cupcake-form').on('submit', async function (event) {
        event.preventDefault();

        const flavor = $('#flavor').val();
        const size = $('#size').val();
        const rating = $('#rating').val();
        const image = $('#image').val() || 'https://tinyurl.com/demo-cupcake';

        const newCupcake = { flavor, size, rating, image };

        const response = await axios.post(BASE_URL, newCupcake);

        $('#cupcakes-list').append(generateCupcakeHTML(response.data.cupcake));
        $('#cupcake-form').trigger('reset');
    });
});
