$(document).ready(function() {
    $('#prediction-form').submit(function(event) {
        event.preventDefault();
        // Get values from inputs
        var price = parseFloat($('#price').val());
        var open = parseFloat($('#open').val());
        var high = parseFloat($('#high').val());
        var low = parseFloat($('#low').val());
        var volume = parseFloat($('#volume').val());
        var change = parseFloat($('#change').val());
        var model = $('#select-option').val();

        // Check if input data is valid
        if (!isNaN(price) && !isNaN(open) && !isNaN(high) && !isNaN(low) && !isNaN(volume) && !isNaN(change)) {
            // Perform prediction 
            $.ajax({
                url: '/predict',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    price: price,
                    open: open,
                    high: high,
                    low: low,
                    volume: volume,
                    change: change,
                    model: model
                }),
                success: function(data) {
                    $('#error-message').hide();
                    $('#success-message').text("The predicted oil price for the next day is: $" + parseFloat(data.price).toFixed(2)).show();
                },
                error: function(xhr, status, error) {
                    $('#success-message').hide();
                    $('#error-message').text(error).show();
                }
            });
        } else {
            alert("Please enter valid numeric values.");
        }
    });
});