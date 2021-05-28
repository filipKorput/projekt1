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

    $addingDirectoryForm.submit(function (e) {
        e.preventDefault();

        let serializedData = $(this).serialize()

        $.ajax({
            type: 'POST',
            url: add_dir_url,
            data: serializedData,
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function (response) {
                $addingDirectoryBox.css('display', 'none');
                $addingDirectoryForm.trigger('reset');
            },
            error: function (response) {
                // alert the error if any error occured
                alert(response["responseJSON"]["error"]);
            }
        })
    })

}