window.onload = () => {

    let selectedFileId = ''
    let selectedDirectoryId = '#'

    const addingDirectoryBox = $('#addingDirectoryBox');
    const $addDirectoryButton = $('#addDirectoryButton');
    const addingDirectoryForm = $('#addingDirectoryForm');


    $addDirectoryButton.on('click', () => {
        addingDirectoryBox.css('display', 'block');
    })


    window.onclick = (e) => {

        if (addingDirectoryBox.is(e.target)) {
            addingDirectoryBox.css('display', 'none');
        }

    }


    addingDirectoryForm.submit((e) => {
        e.preventDefault();

        let serializedData = addingDirectoryForm.serialize()
        serializedData += `&parent_dir_pk=${selectedDirectoryId || '#'}`

        $.ajax({
            type: 'POST',
            url: add_dir_url,
            data: serializedData,
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: (reponse) => {
                $filesystemTree.jstree(true).refresh();
                addingDirectoryBox.css('display', 'none');
                addingDirectoryForm.trigger('reset');
            }
        })
    })

}