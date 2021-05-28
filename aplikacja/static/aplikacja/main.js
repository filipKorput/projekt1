window.onload = () => {

    let selectedFileId = ''
    let selectedDirectoryId = '#'
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const $filesystemTree = $('#fileselection');
    const $focusSection = $('#focus');

    const $addingDirectoryBox = $('#addingDirectoryBox');
    const $directoryButton = $('#addingDirectoryButton');
    const $directoryForm = $('#addingDirectoryForm');



    $directoryButton.on('click', () => {
        $addingDirectoryBox.css('display', 'block');
    })

    window.onclick = (e) => {

        if ($addingDirectoryBox.is(e.target)) {
            $addingDirectoryBox.css('display', 'none');
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
                $addingDirectoryBox.css('display', 'none');
                $directoryForm.trigger('reset');
            }
        })
    })


   const fetchFile = (fileId) => {
       print(${fileId})
        $.ajax({
            type: 'get',
            url: select_file_url,
            data: `file=${fileId}`,
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: (response) => {
                $('#source-code-text-area').val(response.source_code)

                $focusSection.empty()

                for (const section of response.sections) {
                    const key = Number(section.key)
                    $focusSection.append($('<button>').addClass('section-button').attr('id', `focus-button-${key}`).html(section.name).click((event) => {
                        $(`#focus${section.key}`).toggleClass('hide');
                    }));
                    $focusSection.append($('<div>').addClass('section-inner-content').html(section.description).attr('id', `focus${key}`));
                }
            }
        })
    }

    const resetView = () => {
        $('#source-code-text-area').val('')
        $focusSection.empty()
    }

    $filesystemTree
        .on('changed.jstree', (event, data) => {
            const node = data.node

            if (node) {
                if (node.id === '#') {
                    selectedFileId = null
                    selectedDirectoryId = null
                    resetView()
                } else if (node.id.substr(0, 3) === 'dir') {
                    selectedDirectoryId = node.id.substr(3, node.id.length - 3)
                    selectedFileId = null
                    resetView()
                } else {
                    selectedFileId = node.id.substr(3, node.id.length - 3)
                    selectedDirectoryId = node.parent === '#' ? null : node.parent.substr(3, node.parent.length - 3)
                    fetchFile(selectedFileId)
                }
            }
        })
        .jstree({
            'core': {
                'data': {
                    'type': 'GET',
                    'url': url_get_filesystem_tree,
                    'contentType': 'application/json; charset=utf-8',

                    success: (data) => {
                        $(data).each(() => ({'id': this.id, 'parent': this.parent, 'text': this.text}))
                    }
                },
                'plugins': ['state']
            }
        });

}