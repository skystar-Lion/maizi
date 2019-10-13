KindEditor.ready(function(K) {
    window.editor = K.create('#id_content',{
        width:'1000px',
        height:'600px',
        uploadJson: '/admin/upload/kindeditor',
    });
});