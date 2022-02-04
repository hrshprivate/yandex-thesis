$(document).ready(function() {
    $(".form__field-item-delete").on("click", function(e){
        e.preventDefault();
        var $this = $(this);
        if(confirm("Sure to delete?")){
            $.ajax({
            url: $this.attr("href"),
            type: "GET",
            dataType: "json",
            success: function(resp){
                    $this.parents(".form__field-item-ingredient").fadeOut('fast', function(){
                        $this.parents(".form__field-item-ingredient").remove();
                });
            }
        });
    }
    return false;
    });
});