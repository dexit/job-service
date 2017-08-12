  $(document).ready(function() {
    $('#login-form').bootstrapValidator({
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
            }
        }
    })
});
