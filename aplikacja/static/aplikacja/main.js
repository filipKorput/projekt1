window.onload = () => {

    const $directoryModal = $('#new-directory-modal');
    const $directoryButton = $('#new-directory-button');
    const $directoryForm = $('#new-directory-form');


    $directoryButton.on('click', () => {
        $directoryModal.css('display', 'block');
    })


    window.onclick = (e) => {

        if ($directoryModal.is(e.target)) {
            $directoryModal.css('display', 'none');
        }

    }


    $directoryForm.submit((e) => {
        e.preventDefault();

        let serializedData = $directoryForm.serialize()
        serializedData += `&parent_dir_pk=${selectedDirectoryId || '#'}`

        $.ajax({
            type: 'POST',
            url: url_post_new_directory,
            data: serializedData,
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: (reponse) => {
                $filesystemTree.jstree(true).refresh();
                $directoryModal.css('display', 'none');
                $directoryForm.trigger('reset');
            }
        })
    })

}