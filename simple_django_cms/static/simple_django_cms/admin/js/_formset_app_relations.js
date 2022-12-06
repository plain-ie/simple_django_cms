function IamheadlessPublisherAdminRelationChoicesFinder(element, formset){
    this.element = element;
    this.formset = formset;
    //
    this.search_input_element = null;
    this.empty_choice_element = null;
    //
    this.add_trigger_selector = '.iamheadless-publisher-admin-formset-trigger-add-form';
    this.choice_class = 'iamheadless-publisher-admin-formset-choice';
    this.choice_selector = '.' + this.choice_class;
    this.empty_choice_selector = '.iamheadless-publisher-admin-formset-choices-empty-choice';
    this.search_trigger_selector = '.iamheadless-publisher-admin-formset-choices-search-trigger';
    //
    this.clear_rendered_choices = function(){
        var self = this;
        var rendered_choices = self.element.querySelectorAll(self.choice_selector);
        for (var i = 0; i < rendered_choices.length; i++) {
            rendered_choices[i].outerHTML = '';
        };
    };
    //
    this.filter_choices = function(q, choices){
        var filtered_choices = []
        if (q.length === 0){ return [] };
        for (var i = 0; i < choices.length; i++) {
            if (choices[i].title.indexOf(q) !== -1){
                filtered_choices.push(choices[i])
            };
        };
        return filtered_choices;
    };
    this.get_choices = function(q, callback){
        var self = this;

        if (self._cached_choices !== undefined){
            console.log('Returnnig cached choices')
            callback(self.filter_choices(q, self._cached_choices));
            return;
        };

        var url = self.formset.data_choices_url + '&page=1&count=500';
        xhr = new XMLHttpRequest();
        xhr.open('GET', url, true);
        xhr.onload = function() {

            var response = JSON.parse(xhr.response)
            var results = response['results'];

            var formated_choices = [];
            for (var i = 0; i < results.length; i++) {
                formated_choices.push({
                    'id': results[i].id,
                    'title': pick_content(results[i]['data']['contents'], DEFAULT_LANGUAGE).title
                });
            };

            self._cached_choices = formated_choices;

            callback(self.filter_choices(q, self._cached_choices));
            return;

        };
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send();
    };
    this.render_choices = function(keyword){

        var self = this;

        self.clear_rendered_choices();

        var choices = self.get_choices(keyword, function(choices){

            for (var i = 0; i < choices.length; i++) {

                var element = document.createElement('div');

                element.className = self.choice_class;
                element.innerHTML = self.empty_choice_element.innerHTML;

                var input = element.querySelector('input');
                input.value = choices[i].title;

                var trigger = element.querySelector(self.add_trigger_selector);
                trigger.setAttribute('data-choices-id', choices[i].id);
                trigger.setAttribute('data-choices-title', choices[i].title);

                trigger.addEventListener('click', function(event){

                    event.preventDefault();

                    var target = event.target;
                    if (target !== trigger){
                        target = target.parentNode;
                    };

                    var id = target.getAttribute('data-choices-id');
                    var title = target.getAttribute('data-choices-title');

                    self.clear_rendered_choices();
                    self.formset.add_form(id, title);
                    self.search_input_element.value = '';

                });

                self.element.appendChild(element);
            };

        });
    };
    //
    this.detect = function(){
        var self = this;
        self.search_input_element = self.element.querySelector(self.search_trigger_selector);
        self.empty_choice_element = self.element.querySelector(self.empty_choice_selector);
        self.search_input_element.addEventListener('keyup', function(event){
            event.preventDefault();
            var ignore_codes = [9, 13, 39, 37, 38, 40, 17, 16];
            if (ignore_codes.indexOf(event.keyCode) === -1){
                var keyword = self.search_input_element.value;
                self.render_choices(keyword);
            };
        });
    };
    this.init = function(){
        var self = this;
        self.detect();
    };
    this.init();
};


function IamheadlessPublisherAdminRelationFormset(element, controller){
    this.element = element;
    this.controller = controller;
    //
    this.data_choices_url = this.element.getAttribute('data-relation-choices-url');
    this.data_direction = this.element.getAttribute('data-relation-direction');
    this.data_status = this.element.getAttribute('data-relation-status');
    //
    this.choices_finder = null;
    this.empty_form = null;
    this.management_form = null;
    //
    this._empty_form = IamheadlessPublisherAdminFormsetEmptyForm;
    this._form = IamheadlessPublisherAdminFormsetForm;
    this._management_form = IamheadlessPublisherAdminManagementForm;
    //
    this.empty_form_selector = '.iamheadless-publisher-admin-formset-empty-form';
    this.form_selector = '.iamheadless-publisher-admin-formset-form';
    this.management_form_selector = '.iamheadless-publisher-admin-formset-management-form';
    this.formset_choices_selector = '.iamheadless-publisher-admin-formset-choices';
    //
    this.add_form = function(id, title){
        var self = this;
        self.management_form.add_form();
        var prefix = self.management_form.get_total_form_count()
        if (prefix > 0){ prefix -= 1 };

        var new_form = self.empty_form.create_new_form(prefix);

        new_form.querySelector('input[name$=status]').value = self.data_status;
        new_form.querySelector('input[name$=direction]').value = self.data_direction;
        new_form.querySelector('input[name$=item_id]').value = id;
        new_form.querySelector('input[name$=title]').outerHTML = '';
        new_form.querySelector('label[for$=title]').outerHTML = '';
        new_form.querySelector('input[type="text"][disabled]').setAttribute('value', title);

        new self._form(new_form, self)

        self.element.appendChild(new_form);

        self.element.innerHTML = self.element.innerHTML;
        self.init();
    };
    this.remove_form = function(){
        var self = this;
        self.management_form.remove_form();
        self.choices_finder.clear_rendered_choices();
        self.element.innerHTML = self.element.innerHTML;
        self.init();
    };
    this.detect = function(){
        var self = this;

        var management_form_element = self.element.querySelector(self.management_form_selector);
        if (management_form_element !== undefined){
            //
            self.management_form = new self._management_form(management_form_element, self);
            //
            var empty_form_element = self.element.querySelector(self.empty_form_selector);
            if (empty_form_element !== undefined){
                self.empty_form = new self._empty_form(empty_form_element, self);
                document.querySelector('.iamheadless-publisher-admin-form-submit').addEventListener('click', function(e){
                    self.empty_form.element.innerHTML = '';
                });
            };
            //
            var form_elements = self.element.querySelectorAll(self.form_selector);
            for (var i = 0; i < form_elements.length; i++){
                new self._form(form_elements[i], self);
            };
        };

        var choices_search_element = self.element.querySelector(self.formset_choices_selector);
        self.choices_finder = new IamheadlessPublisherAdminRelationChoicesFinder(choices_search_element, self);
    };
    this.init = function(){
        var self = this;
        self.detect();
    };
    this.init();
};
