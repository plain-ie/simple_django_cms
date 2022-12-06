function pick_content(contents, language){
    var content = null;
    for (var i = 0; i < contents.length; i++){
        if (contents[i].language == language){
            return contents[i];
        };
    };
};
