//
// Helpers
//


function string_to_slug(str) {
    // From: https://gist.github.com/codeguy/6684588
    str = str.replace(/^\s+|\s+$/g, '-');
    str = str.toLowerCase();
    var from = "àáäâèéëêìíïîòóöôùúüûñç·/_,:;";
    var to   = "aaaaeeeeiiiioooouuuunc------";
    for (var i=0, l=from.length ; i<l ; i++) {
        str = str.replace(new RegExp(from.charAt(i), 'g'), to.charAt(i));
    };
    str = str.replace(/[^a-z0-9 -]/g, '').replace(/\s+/g, '-').replace(/-+/g, '-');
    return str;
};


//
// Field readability extension
//

var IAMHEADLESS_READABILITY_FORM_FIELD_SELECTOR = '[readability="true"]';
var IAMHEADLESS_READABILITY_FORM_FIELD_SCORE_CLASS_NAME = 'iamheadless_readability_field_readability_score';
var IAMHEADLESS_READABILITY_FORM_FIELD_SCORE_TEXT = 'Score';
var IAMHEADLESS_READABILITY_URL = '#';


function ReadableFormField(field){
    this.field = field;
    this.set_score = function(element, reading_score, reading_ease){
        element.text(IAMHEADLESS_READABILITY_FORM_FIELD_SCORE_TEXT + Math.round(reading_score * 100) / 100);
        element.attr('class', IAMHEADLESS_READABILITY_FORM_FIELD_SCORE_CLASS_NAME + ' ' + reading_ease);
    };
    this.get_score = function(element, value){
        var self = this;
        if (value === undefined || value.length === 0){
            self.set_score(element, 0, 'unset');
            return;
        };
        $.ajax({
            'url': IAMHEADLESS_READABILITY_URL,
            'type': "POST", //send it through get method
            'data': JSON.stringify({
                'text': value,
            }),
            'contentType': "application/json; charset=utf-8",
            'success': function(response) {
                self.set_score(element, response.reading_score, response.reading_ease);
            },
            'error': function(xhr) {
                throw 'Readability AJAX call failed!';
            },
        });
    };
    this.add_score_listener = function(element){
        var self = this;
        var timeout = null;
        var keyup_event = function(event){
            var value = event.target.value;
            if (timeout) {
                clearTimeout(timeout);
            }
            timeout = setTimeout(function() {
                self.get_score(element, value);
            }, 500);
        };
        self.field.off('keyup.keyup_event')
        self.field.keyup(keyup_event);
    };
    this.add_score_output_element = function(){
        var self = this;
        var markup = '<span class="' + IAMHEADLESS_READABILITY_FORM_FIELD_SCORE_CLASS_NAME + '"></span>';
        var element = $(markup);
        self.field.after(element);
        return element;
    };
    this.init = function(){
        var self = this;
        var score_output_element = undefined;
        var selector = '.' + IAMHEADLESS_READABILITY_FORM_FIELD_SCORE_CLASS_NAME;

        var score_output_siblings = self.field.siblings(selector);
        if (score_output_siblings.length === 0){
            score_output_element = self.add_score_output_element();
        } else {
            score_output_element = score_output_siblings.first();
        };

        self.get_score(score_output_element, self.field.val());
        self.add_score_listener(score_output_element);
    };
    this.init();
};


function DetectReadableFormFields(selector){
    this.selector = selector;
    this.init = function(){
        var self = this;
        if (self.selector === undefined) {
            self.selector = IAMHEADLESS_READABILITY_FORM_FIELD_SELECTOR;
        };
        $(self.selector).each(function(index, element){
            new ReadableFormField($(element));
        });
    };
    this.init();
};


//
// Slugfield
//

var IAMHEADLESS_TEXT_TOOLS_SLUG_FIELD_SELECTOR = '[slugfield="true"]';


function FormSlugField(field){
    this.field = field;
    this.add_listener = function(){
        var self = this;
        var keyup_event = function(event){
            self.field.val(string_to_slug(self.field.val()))
        }
        self.field.off('keyup.keyup_event')
        self.field.keyup(keyup_event);
    };
    this.init = function(){
        var self = this;
        self.add_listener();
    };
    this.init();
};

function DetectFormSlugFields(selector){
    this.selector = selector;
    this.init = function(){
        var self = this;
        if (self.selector === undefined) {
            self.selector = IAMHEADLESS_TEXT_TOOLS_SLUG_FIELD_SELECTOR;
        };
        $(self.selector).each(function(index, element){
            new FormSlugField($(element));
        });
    };
    this.init();
};
