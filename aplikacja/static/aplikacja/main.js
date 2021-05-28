window.onload = () => {

    let selectedFileId = ''
    let selectedDirectoryId = '#'
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const $filesystemTree = $('#fileselection');
    const $focusSection = $('#focus');

    const $addingDirectoryBox = $('#addingDirectoryBox');
    const $addingDirectoryButton = $('#addingDirectoryButton');
    const $addingDirectoryForm = $('#addingDirectoryForm');


    $addingDirectoryButton.on('click', () => {
        $addingDirectoryBox.css('display', 'block');
    })

    window.onclick = (e) => {
        if ($addingDirectoryBox.is(e.target)) {
            $addingDirectoryBox.css('display', 'none');
        }
    }

    $addingDirectoryForm.submit((e) => {
        e.preventDefault();

        let serializedData = $addingDirectoryForm.serialize()
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