    var source = document.getElementById('filename');
    var editorWindow = document.getElementById('editor');
    var fileMessage = document.getElementById('file-message');
    var fileStatus = document.getElementById('file-status');
    var fileMessageLOC = document.getElementById('loc');
    var fileMessageBytes = document.getElementById('bytes');
    var fileCursorX = document.getElementById('curX');
    var fileCursorY = document.getElementById('curY');
    var fileSave = document.getElementById('save-btn');
    var fileStore = document.getElementById('store');
    var draftWarning = document.getElementById('draft-warning');

    var keytimers = [];

    var editor = CodeMirror.fromTextArea(editorWindow, {
        styleActiveLine: true,
        lineNumbers: true,
        matchBrackets: true
    });

    source.addEventListener('keyup', function(){
        type = getExt(source.value);
        editor.setOption('mode', type.mime);
        CodeMirror.autoLoadMode(editor, type.mode);
    });

    CodeMirror.modeURL = '{% static "js/codemirror-5.22.0" %}/mode/%N/%N.js';

    editor.setSize(null, window.innerHeight*0.75);
    window.onresize = function(e){
        editor.setSize(null, window.innerHeight*0.75);
    };


    function sendSave(draft=true){
        $.post('/save',{
            filename: source.value,
            code: editor.getValue(),
            loc: editor.getCursor().line+1},
            function(data){
                fileStatus.setAttribute("title", data.dtg);
                fileStatus.innerHTML = data.hash;
                fileStore.innerHTML = data.store;
        });
    }

    $(fileSave).on('click', function(){
        draftWarning.style.display = 'none';
        sendSave();
    });



    editor.on('keyup', function(event){
        keytimers.push(setTimeout(function() {
            sendSave();
        }, 2000));
    });

    editor.on('keydown', function(){
        for (var i = 0; i < keytimers.length; i++) {
            clearTimeout(keytimers[i]);
        }
        keytimers = [];
    });


    editor.on('cursorActivity', function(){
        fileMessageLOC.innerHTML = editor.lineCount();
        fileMessageBytes.innerHTML = editor.getValue().length;

        fileCursorX.innerHTML = editor.getCursor().ch+1;
        fileCursorY.innerHTML = editor.getCursor().line+1;

    });


    editor.on('change', function(){
        if (source.value=='') {
            var draftName = Math.random().toString(36).substr(2,7)+'.md';
            draftWarning.style.display = 'inline-block';
            document.title = draftName + ' draft';
            source.value = draftName;
        }
    });

    function getExt(source){
        var file = source.split('.');
        if (file.length > 1){
            var ext = file[file.length-1]
            var info = CodeMirror.findModeByExtension(ext);
            if (info) {
                return info;
            }
        }
    }
