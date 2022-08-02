
    $('#myChecks').click(function(){
        var is_checked = $(this).is(':checked');
        if(is_checked){
            $("input[type='checkbox']").prop('checked',true)
        }else{
            $("input[type='checkbox']").prop('checked',false)
        }

    })

    $('.model_name').click(function(){
        value = $(this).val()
        var is_checked = $(this).is(':checked');
        if(is_checked){
            $( `.permission-${value}-name`).prop('checked',true)

        }else{
            $( `.permission-${value}-name`).prop('checked',false)
        }
    })

    $('.permissions').click(function(){
        var is_checked = $(this).is(':checked');
        var val_id = $(this).attr('data-id')
        if(is_checked){
            $(`#model_name_${val_id}`).prop('checked',true)
        }
    })
   
    