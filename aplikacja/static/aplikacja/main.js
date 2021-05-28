window.onload = () => {

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const $addingDirectoryBox = $('#addingDirectoryBox');
    const $addingDirectoryButton = $('#addingDirectoryButton');
    const $addingDirectoryForm = $('#addingDirectoryForm');

    const $addingFileBox = $('#addingFileBox');
    const $addingFileButton = $('#addingFileButton');
    const $addingFileForm = $('#addingFileForm');



    $addingDirectoryButton.on('click', () => {
        $addingDirectoryBox.css('display', 'block');
    })

    $addingFileButton.on('click', () => {
        $addingFileBox.css('display', 'block');
    })

    window.onclick = (e) => {
        if ($addingDirectoryBox.is(e.target)) {
            $addingDirectoryBox.css('display', 'none');
        }

        if ($addingFileBox.is(e.target)) {
            $addingFileBox.css('display', 'none');
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

    $addingFileForm.submit(function (e) {
        e.preventDefault();

        let serializedData = $(this).serialize()

        $.ajax({
            type: 'POST',
            url: add_file_url,
            data: serializedData,
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function (response) {
                $addingFileBox.css('display', 'none');
                $addingFileForm.trigger('reset');
            },
            error: function (response) {
                // alert the error if any error occured
                alert(response["responseJSON"]["error"]);
            }
        })
    })


}