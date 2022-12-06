function IamheadlessPublisherAdminFormsetForm(element, formset){
    this.element = element;
    this.formset = formset;
    this.remove_form = function(){
        var self = this;
        self.element.outerHTML = '';
        self.formset.remove_form();
    };
    this.set_remove_listener = function(){
        var self = this;
        var selector = '.iamheadless-publisher-admin-formset-trigger-remove-form';
        var trigger_elements = self.element.querySelectorAll(selector);
        for (var i = 0; i < trigger_elements.length; i++){
            trigger_elements[i].addEventListener('click', function(event){
                self.remove_form();
                event.preventDefault();
            });
        };
    }
    this.set_remove_listener()
};


function IamheadlessPublisherAdminFormsetEmptyForm(element, formset){
    this.element = element;
    this.formset = formset;
    this.create_new_form = function(prefix){
        var self = this;
        var selector = 'iamheadless-publisher-admin-formset-form';
        var element = document.createElement('div');
        element.className = selector;
        element.innerHTML = self.element.innerHTML;
        var inputs = element.querySelectorAll('[name]');
        for (var i = 0; i < inputs.length; i++){
            inputs[i].name = inputs[i].name.replace('__prefix__', prefix);
            inputs[i].id = inputs[i].id.replace('__prefix__', prefix);
        };
        return element;
    };
};


function IamheadlessPublisherAdminManagementForm(element, formset){
    this.element = element;
    this.formset = formset;
    //
    this.initial_forms_element = null;
    this.minimum_forms_element = null;
    this.maximum_forms_element = null;
    this.total_forms_element = null;
    //
    this.add_form = function(){
        var self = this;
        var current_value = parseInt(self.total_forms_element.value)
        var new_value = current_value + 1;
        self.total_forms_element.value = new_value;
    }
    this.remove_form = function(){
        var self = this;
        var current_value = parseInt(self.total_forms_element.value)
        var new_value = current_value - 1;
        if (new_value < 0) { new_value = 0 };
        self.total_forms_element.value = new_value;
    };
    this.get_total_form_count = function(){
        var self = this;
        return self.total_forms_element.value;
    };
    this.detect = function(){
        var self = this;
        this.initial_forms_element = self.element.querySelector('input[name$=INITIAL_FORMS]');
        this.minimum_forms_element = self.element.querySelector('input[name$=MIN_NUM_FORMS]');
        this.maximum_forms_element = self.element.querySelector('input[name$=MAX_NUM_FORMS]');
        this.total_forms_element = self.element.querySelector('input[name$=TOTAL_FORMS]');
    };
    this.init = function(){
        var self = this;
        self.detect();
    };
    this.init();
};


function IamheadlessPublisherAdminFormset(element, controller){
    this.element = element;
    this.controller = controller;
    //
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
    //
    this.get_appendChild_element = function(){
        var self = this;
        return self.element;
    };
    //
    this.set_add_form_listener = function(){
        var self = this;
        var selector = '.iamheadless-publisher-admin-formset-trigger-add-form';
        var trigger_elements = self.element.querySelectorAll(selector);
        for (var i = 0; i < trigger_elements.length; i++){
            trigger_elements[i].addEventListener('click', function(event){
                self.add_form();
                event.preventDefault();
            });
        };
    };
    this.add_form = function(){
        var self = this;

        self.management_form.add_form();

        var prefix = self.management_form.get_total_form_count();
        if (prefix > 0){ prefix -= 1 };

        var new_form = self.empty_form.create_new_form(prefix);
        new self._form(new_form, self)

        var append_to_element = self.get_appendChild_element();
        append_to_element.appendChild(new_form);

        self.element.innerHTML = self.element.innerHTML;
        self.init();
    };
    this.remove_form = function(){
        var self = this;
        self.management_form.remove_form();
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
            };
            //
            var form_elements = self.element.querySelectorAll(self.form_selector);
            for (var i = 0; i < form_elements.length; i++){
                new self._form(form_elements[i], self);
            };
        };
    };
    this.init = function(){
        var self = this;
        self.detect();
        self.set_add_form_listener();
    };
    this.init();
};


function IamheadlessPublisherAdminFormsetController(_formset, formset_selector){
    this._formset = _formset;
    this.formset_selector = formset_selector;
    //
    this.detect = function(){
        var self = this;
        var formset_elements = document.querySelectorAll(self.formset_selector, self);
        for (var i = 0; i < formset_elements.length; i++){
            new self._formset(formset_elements[i], self);
        };
    };
    this.init = function(){
        var self = this;
        self.detect();
    };
    this.init();
};
