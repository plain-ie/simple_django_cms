function language_formset_after_detect_formset_function(form_element){
    // This is function to run after formset translatable content formset is detected.
    // Use this function to add custom behavior
}


function IamheadlessPublisherAdminLanguageFormset(element, controller){
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
    this.set_add_form_listener = function(){
        var self = this;
        var selector = '.iamheadless-publisher-admin-formset-trigger-add-form';
        var trigger_elements = self.element.querySelectorAll(selector);
        for (var i = 0; i < trigger_elements.length; i++){
            trigger_elements[i].addEventListener('click', function(event){
                var language_code = event.target.getAttribute('data-language-code');
                self.add_form(language_code);
                event.preventDefault();
            });
        };
    }
    this.add_form = function(language){
        var self = this;
        self.management_form.add_form();
        var prefix = self.management_form.get_total_form_count()
        if (prefix > 0){ prefix -= 1 };
        // Add tab
        var empty_tab_li = self.element.querySelector('.iamheadless-publisher-admin-formset-empty-tab li');
        var new_tab = document.createElement('li');
        new_tab.setAttribute('role', 'presentation');
        new_tab.innerHTML = empty_tab_li.innerHTML;
        //
        var new_tab_link = new_tab.querySelector('a');
        var new_tab_link_href = new_tab_link.getAttribute('href')
        var new_tab_link_aria_controls = new_tab_link.getAttribute('aria-controls')
        //
        new_tab_link.setAttribute('href', new_tab_link_href.replace('__prefix__', prefix));
        new_tab_link.setAttribute('aria-controls', new_tab_link_aria_controls.replace('__prefix__', prefix));
        new_tab_link.innerHTML = language.toUpperCase();
        //
        self.element.querySelector('ul.nav-tabs').appendChild(new_tab);
        // Add listener from bootstrap
        $(new_tab_link).click(function (e) {
            e.preventDefault()
            $(this).tab('show')
        });
        // Add form
        var new_form = self.empty_form.create_new_form(prefix)
        //
        var new_form_pane = document.createElement('div');
        new_form_pane.setAttribute('role', 'tabpanel');
        new_form_pane.setAttribute('class', 'tab-pane iamheadless-publisher-admin-formset-form');
        new_form_pane.setAttribute('id', prefix + '-content-formset');
        new_form_pane.innerHTML = new_form.innerHTML;
        new_form_pane.querySelector('input[name$="-language"]').setAttribute('value', language);
        //
        self.element.querySelector('.tab-content').appendChild(new_form_pane)
        new self._form(new_form_pane, self)
        self.element.innerHTML = self.element.innerHTML;
        self.init();
    };
    this.remove_form = function(){
        var self = this;
        self.management_form.remove_form();
        var id = self.element.getAttribute('id');
        self.element.querySelector('li.active').innerHTML = '';
        self.element.innerHTML = self.element.innerHTML;
        self.init();
        // Show first tab
        var tabs = self.element.querySelectorAll('ul.nav-tabs li[role="presentation"] a');
        $(tabs[0]).tab('show');
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
                language_formset_after_detect_formset_function(form_elements[i]);
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
