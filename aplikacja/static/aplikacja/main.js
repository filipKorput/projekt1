window.onload = () => {

    let selectedFile = ''

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

    const $rerunFramaButton = $('#rerunFramaButton');
    const $fileTree = $('#fileselection');


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

        let data = new FormData(this); //get data of form elements for submission

        $.ajax({
            type: 'POST',
            url: add_file_url,
            enctype: 'multipart/form-data',
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


    $fileTree
        .on('changed.jstree', (event, data) => {
            const node = data.node

            if (node) {
                if (node.id === '') {
                    selectedFile = null

                    $('#textFieldContent').empty()
                    $('#title').empty()
                    $('#resultContent').empty()
                    $('.focus').empty()
                } else {
                    selectedFile = node.id.substr(3, node.id.length - 3)
                    getFile(selectedFile)
                }
            }
        })
        .jstree({
            'core': {
                'data': {
                    'type': 'GET',
                    'url': url_get_fileTree,
                    'contentType': 'application/json; charset=utf-8',

                    success: (data) => {
                        $(data).each(() => ({'id': this.id, 'parent': this.parent, 'text': this.text}))
                    }
                },
                'plugins': ['state']
            }
        });


    const getFile = (fileName) => {

         //let val = $(this).attr('value');
         //console.log(val)

         $.ajax({
             type: 'POST',
             url: select_file_url,
             data: 'fileName=${fileName}',
             headers: {
                'X-CSRFToken': csrftoken
             },
             success: (response) => {
                 selectedFile = response.title
                 $('#textFieldContent').html(response.fileContent)
                 $('#title').text(response.title)
                 $('#resultContent').html(response.summary)

                 $('.focus').empty()

                 for (const section of response.sectionList) {
                     $('<div/>', { 'class': "section " + section[1] }).appendTo($('.focus')).append($('<button>').attr('type', 'button').addClass('collapsible').html(section[2] + " - " + section[1]).click(function() {
                     $(this.classList).toggle("active");
                     let content = this.nextElementSibling;
                     if (content.style.display === "block") {
                       content.style.display = "none";
                     } else {
                       content.style.display = "block";
                     }
                     })).append($('<div>').addClass('section_content').html("<pre>" + section[0] + "</pre>"));
                     ($('.focus')).append($('<p>').text("------------------------------------------------------------"));
                 }

                 let coll = document.getElementsByClassName("collapsible");
                let i;

                for (i = 0; i < coll.length; i++) {
                  coll[i].addEventListener("click", function() {
                    this.classList.toggle("active");
                    let content = this.nextElementSibling;
                    if (content.style.display === "block") {
                      content.style.display = "none";
                    } else {
                      content.style.display = "block";
                    }
                  });
                }

             }

         });

    }


    $(".collapsible").click(function() {

        $(this.classList).toggle("active");
        let content = this.nextElementSibling;
        if (content.style.display === "block") {
          content.style.display = "none";
        } else {
          content.style.display = "block";
        }

    });



    $rerunFramaButton.on('click', () => {

        $.ajax({
            type: 'POST',
            url: rerun_frama_url,
            data: '&fileName=' + selectedFile,
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function (response) {
                selectedFile = response.title
                $('#textFieldContent').html(response.fileContent)
                $('#title').text(response.title)
                $('#resultContent').html(response.summary)

                $('.focus').empty()

                 for (const section of response.sectionList) {
                     $('<div/>', { 'class': "section " + section[1] }).appendTo($('.focus')).append($('<button>').attr('type', 'button').addClass('collapsible').html(section[2] + " - " + section[1]).click(function() {
                     $(this.classList).toggle("active");
                     let content = this.nextElementSibling;
                     if (content.style.display === "block") {
                       content.style.display = "none";
                     } else {
                       content.style.display = "block";
                     }
                     })).append($('<div>').addClass('section_content').html("<pre>" + section[0] + "</pre>"));
                     ($('.focus')).append($('<p>').text("------------------------------------------------------------"));
                 }

                 let coll = document.getElementsByClassName("collapsible");
                let i;

                for (i = 0; i < coll.length; i++) {
                  coll[i].addEventListener("click", function() {
                    this.classList.toggle("active");
                    let content = this.nextElementSibling;
                    if (content.style.display === "block") {
                      content.style.display = "none";
                    } else {
                      content.style.display = "block";
                    }
                  });
                }

            },
            error: function (response) {
                alert(response["responseJSON"]["error"]);
            }
        })
    })

}