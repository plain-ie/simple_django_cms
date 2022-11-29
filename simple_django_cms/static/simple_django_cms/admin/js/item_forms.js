function EmptyTranslatableContentForm(parent){
    this.parent = parent;
    this.selector = '.formset-empty-form';
    this.object = null;
    //
    this.get_fresh_form = function(language, index){
        var self = this;

        var form = self.object.find('.tab-pane').first().clone();

        var id = form.attr('id');
        form.attr('id', id.replace('__prefix__', index))

        var inner_html = form.html().replaceAll('__prefix__', index)
        form.html(inner_html)

        var language_input = form.find(
            'input[name=form-' + index + '-language]'
        ).first().val(language);

        form.find(self.parent.remove_trigger_selector).each(function(){
            $(this).click(function(event){
                self.parent.remove(language, index);
                event.preventDefault();
            });
        });

        return form
    };
    //
    this.detect = function(){
        var self = this;
        object = self.parent.object.find(self.selector).first();
        self.object = object.clone();
        object.remove();
    };
};


function ManagementForm(parent){
    this.parent = parent;
    this.selector = '.formset-management-form';
    this.object = null;
    this.initial_forms_object = null;
    this.minimum_forms_object = null;
    this.maximum_forms_object = null;
    this.total_forms_object = null;
    //
    this.set_initial_forms_object = function(){
        var self = this;
        if (self.object !== null){
            self.initial_forms_object = self.object.find(
                'input[name$=INITIAL_FORMS]'
            ).first();
        };
    };
    this.set_minimum_forms_object = function(){
        var self = this;
        if (self.object !== null){
            self.minimum_forms_object = self.object.find(
                'input[name$=MIN_NUM_FORMS]'
            ).first();
        };
    };
    this.set_maximum_forms_object = function(){
        var self = this;
        if (self.object !== null){
            self.maximum_forms_object = self.object.find(
                'input[name$=MAX_NUM_FORMS]'
            ).first();
        };
    };
    this.set_total_forms_object = function(){
        var self = this;
        if (self.object !== null){
            self.total_forms_object = self.object.find(
                'input[name$=TOTAL_FORMS]'
            ).first();
        };
    };
    //
    this.get_maximum_forms_count = function(){
        var self = this;
        return parseInt(self.maximum_forms_object.val())
    };
    this.get_total_forms_count = function(){
        var self = this;
        return parseInt(self.total_forms_object.val())
    };
    this.set_total_forms_count = function(value){
        var self = this;
        self.total_forms_object.val(value);
    };
    this.allow_add = function(){
        var self = this;
        return self.get_total_forms_count() < self.get_maximum_forms_count();
    };
    this.allow_remove = function(){
        var self = this;
        return self.get_total_forms_count() > 0;
    };
    //
    this.add = function(){
        var self = this;
        var current_value = self.get_total_forms_count();
        var new_value = current_value + 1;
        self.set_total_forms_count(new_value);
    }
    this.remove = function(){
        var self = this;
        var current_value = self.get_total_forms_count();
        var new_value = current_value - 1;
        if (new_value < 0) { new_value = 0 };
        self.set_total_forms_count(new_value);
    };
    //
    this.detect = function(){
        var self = this;
        var objects = self.parent.object.find(self.selector);
        if (objects.length === 1){
            self.object = objects.first();
            self.set_initial_forms_object();
            self.set_minimum_forms_object();
            self.set_maximum_forms_object();
            self.set_total_forms_object();
        }
    };
};


function EmptyTranslatableContentTab(parent){
    this.parent = parent;
    this.selector = '.formset-empty-tab';
    this.object = null;
    //
    this.get_fresh_tab = function(language, index){
        var self = this;

        var tab = self.object.find('li').first().clone();
        var tab_link = tab.find('a').first();

        var href = tab_link.attr('href');
        var aria_controls = tab_link.attr('aria-controls');

        tab_link.attr('href', href.replace('__prefix__', index));
        tab_link.attr('aria-controls', aria_controls.replace('__prefix__', index));
        tab_link.text(language.toUpperCase());

        return tab;
    }
    //
    this.detect = function(){
        var self = this;
        var objects = self.parent.object.find(self.selector);
        if (objects.length === 1){
            self.object = objects.first();
        };
    };
};


function TranslatableContentFormset(){
    this.remove_trigger_selector = '.formset-trigger-remove-form';
    this.add_trigger_selector = '.formset-trigger-add-form';
    this.selector = '.formset-translatable-contents';
    this.object = null;
    this.empty_form = null;
    this.empty_tab = null;
    this.management_form = null;
    //
    this.listen_for_add_event = function(){
        var self = this;
        self.object.find(self.add_trigger_selector).each(function(){
            $(this).click(function(event){
                self.add($(this).attr('data-language-code'));
                event.preventDefault();
            });
        });
    };
    //
    this.add_form = function(language, index){
        var self = this;
        var forms_container = self.object.find('.tab-content').first();
        var form = self.empty_form.get_fresh_form(language, index);
        forms_container.append(form);
    };
    this.add_tab = function(language, index){
        var self = this;
        var tabs_container = self.object.find('ul.nav.nav-tabs').first();
        var tabs = tabs_container.find('li[role$=presentation]');
        var new_tab = self.empty_tab.get_fresh_tab(language, index);
        new_tab.insertBefore(tabs.last());
    };
    this.remove_tab = function(language, index){
        var self = this;
        var tabs_container = self.object.find('ul.nav.nav-tabs').first();
        var tabs = tabs_container.find('li');
        var selector = 'a[aria-controls=' + index + '-content-formset]';
        var tab = tabs.find(selector).first()
        tab.parent().remove();
        tabs.first().addClass('active')
    };
    this.remove_form = function(language, index){
        var self = this;
        var forms_container = self.object.find('.tab-content').first();
        var forms = forms_container.find('.tab-pane');
        var selector = '#' + index + '-content-formset';
        forms_container.find(selector).remove();
        forms.first().addClass('active')
    };
    //
    this.add = function(language){
        var self = this;
        if (self.management_form.allow_add() === true){
            self.management_form.add();
            var index = self.management_form.get_total_forms_count() - 1;
            if (index < 0){
                index = 0;
            };
            self.add_tab(language, index);
            self.add_form(language, index);
        };
    };
    this.remove = function(language, index){
        var self = this;
        if (self.management_form.allow_remove() === true){
            self.management_form.remove();
            self.remove_tab(language, index);
            self.remove_form(language, index);
        };
    };
    //
    this.detect = function(){
        var self = this;
        var objects = $(self.selector);
        if (objects.length === 1){

            self.object = objects.first();

            self.management_form = new ManagementForm(self)
            self.management_form.detect();

            self.empty_form = new EmptyTranslatableContentForm(self);
            self.empty_form.detect();

            self.empty_tab = new EmptyTranslatableContentTab(self);
            self.empty_tab.detect();

            self.listen_for_add_event();

        };
    };
};


$(document).ready(function(){

    new TranslatableContentFormset().detect();

});
