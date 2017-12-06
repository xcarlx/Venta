
    function actionFormatter(value, row, index) {
        return [
            '<a class="edit ml10" href="javascript:void(0)" title="Edit">',
            '<i class="fa fa-edit"></i>',
            '</a>',
            '<a class="remove ml10" href="javascript:void(0)" title="Remove">',
            '<i class="fa fa-remove"></i>',
            '</a>'
        ].join('');
    }

    window.actionEvents = {
        'click .edit': function (e, value, row, index) {
            idmodelo = row.id;
            urleditar = urlformulario.replace(/12345/, idmodelo);
            modalweb.find(".modal-body").load(urleditar);
            modalweb.find('h4').text("Ediar "+modelo);
            modalweb.modal('show');
        },
        'click .remove': function (e, value, row, index) {
            idmodelo = row.id;
            modalweb.modal('show');
            urleditar = urlformularioeliminar.replace(/12345/, idmodelo);
            modalweb.find(".modal-body").load(urleditar);
            modalweb.find('h4').text("Eliminar "+modelo);
            $("#idBotonModal").text("Eliminar");
        }
    };

     modalweb.on('shown.bs.modal', function () {

    });

    btnNuevo.on('click', function () {
        idmodelo = 0;
        modalweb.find('h4').html('<i class="fa fa-fw fa-lg fa-check-circle" ></i>');
        modalweb.find('h4').text("Nueva "+modelo);
        modalweb.modal('show');
        urleditar = urlformulario.replace(/12345/, idmodelo);
        modalweb.find(".modal-body").load(urleditar);

    });
    formulario.submit(function( event ) {
        $.post(urleditar, $(this).serialize())
           .done(function( data ) {
               if(data.estado){
                   $.notify({
                       title: "Mensaje: ",
                       message: data.mensaje,
                       icon: 'fa fa-check'
                   },{
                       type: "info"
                   });
                   modalweb.modal('hide');

               }else{
                   modalweb.find(".modal-body").html(data)
               }
            tabla.bootstrapTable('refresh');

           });
        event.preventDefault();
    });
    modalweb.on('hidden.bs.modal', function (e) {
        $("#idBotonModal").text("Guardar");
    });