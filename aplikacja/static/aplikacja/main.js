window.onload = () => {

    let selectedFileId = ''
    let selectedDirectoryId = '#'
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const $filesystemTree = $('#fileselection');
    const $focusSection = $('#focus');

    const $addingDirectoryBox = $('#addingDirectoryBox');
    const $addingDirectoryButton = $('#addingDirectoryButton');
    const $directoryForm = $('#addingDirectoryForm');


    $addingDirectoryButton.on('click', () => {
        $addingDirectoryBox.css('display', 'block');
    })

}