
function populateCarriers(elementId) {
    var url = $SCRIPT_ROOT + "/getCarriers";
    $.getJSON(url, function (data) {
        var option = '';
        $.each(data , function(id,name) {
            option += '<option value="' + id + '">' + name + '</option>';
        });
        $(elementId).append(option);
    })

}