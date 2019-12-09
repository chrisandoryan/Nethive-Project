'use strict'

// Make the dashboard widgets sortable Using jquery UI
$('.connectedSortable').sortable({
    placeholder         : 'sort-highlight',
    connectWith         : '.connectedSortable',
    handle              : '.card-header, .nav-tabs',
    forcePlaceholderSize: true,
    zIndex              : 999999
})
$('.connectedSortable .card-header, .connectedSortable .nav-tabs-custom').css('cursor', 'move')

// jQuery UI sortable for the todo list
$('.todo-list').sortable({
    placeholder         : 'sort-highlight',
    handle              : '.handle',
    forcePlaceholderSize: true,
    zIndex              : 999999
})


// Creating DataTable for ConfigurationPage
$('#historian').DataTable({
    "paging": false,
    "lengthChange": false,
    "searching": true,
    "ordering": true,
    "info": false,
    "autoWidth": false,
});
$('#audit').DataTable({
    "paging": false,
    "lengthChange": false,
    "searching": true,
    "ordering": true,
    "info": false,
    "autoWidth": false,
});

// search input CSS
$('#audit_filter input').addClass('form-control');
$('#historian_filter input','').addClass('form-control');
