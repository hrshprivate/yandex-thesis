$("#addIng").click(
        function (e) {
            e.preventDefault();
                         // Получить значение
            asd = $("#nameIngredient").val();
            privet = $("#cantidad").val();
            var token =  $('input[name="csrfToken"]').attr('value')
            if ((!asd) || (!privet)) {

                    swal("Bad!", "Не заполнили поля!", "error");
                    return false;
                    }
            //url = "/ajax_post_data/?username="+username+"&password=" + password;
                         // Построить словарь данных
            send_data = {
                "asd":asd,
                "privet":privet,
            };
            alert('send_data')
            url = "/send";
            $.ajax(
                {
                    url:url,
                    type:"post",
                    data:send_data,
                    headers: {
                    'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value
    },
                    success:function (data) {
                        alert('data');
                        console.log(data.content);
                        $("#text").text(data.content);

                    },
                    error:function (error) {
                        alert('error');
                    }
                }
            )

        }
    )