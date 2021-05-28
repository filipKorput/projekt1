window.onload = () => {

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const $addingDirectoryBox = $('#addingDirectoryBox');
    const $addingDirectoryButton = $('#addingDirectoryButton');
    const $addingDirectoryForm = $('#addingDirectoryForm');

    const $addingFileBox = $('#addingFileBox');
    const $addingFileButton = $('#addingFileButton');
    const $addingFileForm = $('#addingFileForm');

    const $deletingDirectoryBox = $('#deletingDirectoryBox');
    const $deletingDirectoryButton = $('#deletingDirectoryButton');
    const $deletingDirectoryForm = $('#deletingDirectoryForm');

    const $deletingFileBox = $('#deletingFileBox');
    const $deletingFileButton = $('#deletingFileButton');
    const $deletingFileForm = $('#deletingFileForm');


    $addingDirectoryButton.on('click', () => {
        $addingDirectoryBox.css('display', 'block');
    })

    $addingFileButton.on('click', () => {
        $addingFileBox.css('display', 'block');
    })

    $deletingDirectoryButton.on('click', () => {
        $deletingDirectoryBox.css('display', 'block');
    })

    $deletingFileButton.on('click', () => {
        $deletingFileBox.css('display', 'block');
    })

    window.onclick = (e) => {
        if ($addingDirectoryBox.is(e.target)) {
            $addingDirectoryBox.css('display', 'none');
        }

        if ($addingFileBox.is(e.target)) {
            $addingFileBox.css('display', 'none');
        }

        if ($deletingDirectoryBox.is(e.target)) {
            $deletingDirectoryBox.css('display', 'none');
        }

        if ($deletingFileBox.is(e.target)) {
            $deletingFileBox.css('display', 'none');
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

        let data = new FormData($('form').get(0));

        let f_obj = $("#blob").get(0).files[0];
        console.log("File object:", f_obj);

        data.append("uploadedFile", f_obj)

        $.ajax({
            type: 'POST',
            url: add_file_url,
            data: data,
            cache: false,
            processData:false,
            contentType:false,
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

    $deletingDirectoryForm.submit(function (e) {
        e.preventDefault();

        let serializedData = $(this).serialize()

        $.ajax({
            type: 'POST',
            url: delete_dir_url,
            data: serializedData,
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function (response) {
                $deletingDirectoryBox.css('display', 'none');
                $deletingDirectoryForm.trigger('reset');
            },
            error: function (response) {
                // alert the error if any error occured
                alert(response["responseJSON"]["error"]);
            }
        })
    })

    $deletingFileForm.submit(function (e) {
        e.preventDefault();

        let serializedData = $(this).serialize()

        $.ajax({
            type: 'POST',
            url: delete_file_url,
            data: serializedData,
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function (response) {
                $deletingFileBox.css('display', 'none');
                $deletingFileForm.trigger('reset');
            },
            error: function (response) {
                // alert the error if any error occured
                alert(response["responseJSON"]["error"]);
            }
        })
    })

}