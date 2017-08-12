  $(document).ready(function() {
    $('#sign-up-form').bootstrapValidator({
        // To use feedback icons, ensure that you use Bootstrap v3.1.0 or later
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            name: {
                validators: {
                        stringLength: {
                        min: 2
                    },
                        notEmpty: {
                        message: 'Please supply a name'
                    }
                }
            },
             password: {
                validators: {
                     stringLength: {
                        min: 8
                    },
                    notEmpty: {
                        message: 'Please supply a password'
                    }
                }
            },
            email: {
                validators: {
                    notEmpty: {
                        message: 'Please supply your email address'
                    },
                    emailAddress: {
                        message: 'Please supply a valid email address'
                    }
                }
            },
            phone: {
                validators: {
                    notEmpty: {
                        message: 'Please supply your phone number'
                    },
                    phone: {
                        country: 'US',
                        message: 'Please supply a vaild phone number with area code'
                    }
                }
            },
            "company_details.registration_number": {
                validators: {
                    notEmpty: {
                        message: 'Please supply your company registration number'
                    }
                }
            }
            }
        })
});
