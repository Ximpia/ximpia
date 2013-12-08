Templates
=========

Our templates are plain html5 files with visual components as ``div`` elements and variable
placeholders with ``{{}}`` notation, providing a logic-less template system.

You can place conditions inside ``Container`` visual component. You set conditions in view
definition and attach rendering actions to conditions defined.

.. code-block:: html

    <!DOCTYPE html>
    <html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>Ximpia - Change Password</title>
    </head>
    <body>
    <div id="id_popup" 
            data-xp="{title: 'Change Password'}" ></div>
    <!-- Content -->
    <section id="id_content" class="sectionContent">
    <div id="id_changePassword">
    <form id="form_userChangePassword" action="" method="post" data-xp="{}">
    <!-- ximpiaId -->
    <div id="id_username_comp" 
            data-xp-type="field" 
            data-xp="{tabindex: '1', label: 'XimpiaId', 'readonly': 'readonly'}" > </div>
    <!-- password -->
    <div id="id_password_comp" data-xp-type="field"  style="margin-top: 10px"
            data-xp="{type: 'password', info: true}" ></div>
    <!-- newPassword -->
    <div id="id_newPassword_comp" data-xp-type="field" style="margin-top: 10px" 
            data-xp="{type: 'password', info: true, class: 'passwordStrength'}" ></div>
    <!-- newPasswordConfirm -->
    <div id="id_newPasswordConfirm_comp" data-xp-type="field" style="margin-top: 10px"
            data-xp="{type: 'password', info: true}" ></div>
    </form>
    </div>
    <br/>
    </section>
    <!-- Content -->
    <!-- Page Button Bar -->
    <section id="id_sectionButton" class="sectionButton">
    <div id="id_popupButton" class="btBar">
    <div id="id_doChangePassword_comp" data-xp-type="button" 
                    data-xp="{  form: 'form_userChangePassword', 
                                align: 'right', 
                                text: 'Save', 
                                type: 'iconPopup', 
                                mode: 'actionMsg', 
                                action: 'changePassword', 
                                clickStatus: 'disable', 
                                icon: 'save'}" ></div>
    </div>
    </section>
    <!-- Page Button Bar -->
    </body>
    </html>

Visual Context
--------------

Server-side data is serialized into a visual context, a ``JSON`` data entity having forms, lists
and other attributes you may insert from your service views and actions.

Example visual context for ximpia.com home page:

.. code-block:: json

    {   'errors': [],
        'response': {   'app': 'ximpia_site',
                        'appSlug': u'front',
                        'defaultApp': 'front',
                        'form_home': {   'ERR_GEN_VALIDATION': {   'class': 'field',
                                                                   'data-xp-type': 'input.hidden',
                                                                   'fieldType': 'HiddenField',
                                                                   'helpText': u'',
                                                                   'jsRequired': None,
                                                                   'label': None,
                                                                   'name': 'ERR_GEN_VALIDATION',
                                                                   'required': None,
                                                                   'type': 'hidden',
                                                                   'value': u'Error validating your data. Check errors marked in red'},
                                         'action': {   'class': 'field',
                                                       'data-xp-type': 'input.hidden',
                                                       'fieldType': 'HiddenField',
                                                       'helpText': u'',
                                                       'jsRequired': None,
                                                       'label': None,
                                                       'name': 'action',
                                                       'required': None,
                                                       'type': 'hidden',
                                                       'value': ''},
                                         'app': {   'class': 'field',
                                                    'data-xp-type': 'input.hidden',
                                                    'fieldType': 'HiddenField',
                                                    'helpText': u'',
                                                    'jsRequired': None,
                                                    'label': None,
                                                    'name': 'app',
                                                    'required': None,
                                                    'type': 'hidden',
                                                    'value': 'ximpia_site'},
                                         'buttonConstants': {   'class': 'field',
                                                                'data-xp-type': 'input.hidden',
                                                                'fieldType': 'HiddenField',
                                                                'helpText': u'',
                                                                'jsRequired': None,
                                                                'label': None,
                                                                'name': 'buttonConstants',
                                                                'required': None,
                                                                'type': 'hidden',
                                                                'value': u"[['close','Close']]"},
                                         'choices': {   'class': 'field',
                                                        'data-xp-type': 'input.hidden',
                                                        'fieldType': 'HiddenField',
                                                        'helpText': u'',
                                                        'jsRequired': None,
                                                        'label': None,
                                                        'name': 'choices',
                                                        'required': None,
                                                        'type': 'hidden',
                                                        'value': '{}'},
                                         'dbObjects': {   'class': 'field',
                                                          'data-xp-type': 'input.hidden',
                                                          'fieldType': 'HiddenField',
                                                          'helpText': u'',
                                                          'jsRequired': None,
                                                          'label': None,
                                                          'name': 'dbObjects',
                                                          'required': None,
                                                          'type': 'hidden',
                                                          'value': '{}'},
                                         'entryFields': {   'class': 'field',
                                                            'data-xp-type': 'input.hidden',
                                                            'fieldType': 'HiddenField',
                                                            'helpText': u'',
                                                            'jsRequired': None,
                                                            'label': None,
                                                            'name': 'entryFields',
                                                            'required': None,
                                                            'type': 'hidden',
                                                            'value': '{}'},
                                         'errorMessages': {   'class': 'field',
                                                              'data-xp-type': 'input.hidden',
                                                              'fieldType': 'HiddenField',
                                                              'helpText': u'',
                                                              'jsRequired': None,
                                                              'label': None,
                                                              'name': 'errorMessages',
                                                              'required': None,
                                                              'type': 'hidden',
                                                              'value': '{}'},
                                         'facebookAppId': {   'class': 'field',
                                                              'data-xp-type': 'input.hidden',
                                                              'fieldType': 'HiddenField',
                                                              'helpText': u'',
                                                              'jsRequired': None,
                                                              'label': None,
                                                              'name': 'facebookAppId',
                                                              'required': None,
                                                              'type': 'hidden',
                                                              'value': ''},
                                         'msg_ok': {   'class': 'field',
                                                       'data-xp-type': 'input.hidden',
                                                       'fieldType': 'HiddenField',
                                                       'helpText': u'',
                                                       'jsRequired': None,
                                                       'label': None,
                                                       'name': 'msg_ok',
                                                       'required': None,
                                                       'type': 'hidden',
                                                       'value': u' '},
                                         'okMessages': {   'class': 'field',
                                                           'data-xp-type': 'input.hidden',
                                                           'fieldType': 'HiddenField',
                                                           'helpText': u'',
                                                           'jsRequired': None,
                                                           'label': None,
                                                           'name': 'okMessages',
                                                           'required': None,
                                                           'type': 'hidden',
                                                           'value': '{}'},
                                         'params': {   'class': 'field',
                                                       'data-xp-type': 'input.hidden',
                                                       'fieldType': 'HiddenField',
                                                       'helpText': u'',
                                                       'jsRequired': None,
                                                       'label': None,
                                                       'name': 'params',
                                                       'required': None,
                                                       'type': 'hidden',
                                                       'value': '{"viewMode": ["update", "delete"]}'},
                                         'pkFields': {   'class': 'field',
                                                         'data-xp-type': 'input.hidden',
                                                         'fieldType': 'HiddenField',
                                                         'helpText': u'',
                                                         'jsRequired': None,
                                                         'label': None,
                                                         'name': 'pkFields',
                                                         'required': None,
                                                         'type': 'hidden',
                                                         'value': '{}'},
                                         'result': {   'class': 'field',
                                                       'data-xp-type': 'input.hidden',
                                                       'fieldType': 'HiddenField',
                                                       'helpText': u'',
                                                       'jsRequired': None,
                                                       'label': None,
                                                       'name': 'result',
                                                       'required': None,
                                                       'type': 'hidden',
                                                       'value': ' '},
                                         'siteMedia': {   'class': 'field',
                                                          'data-xp-type': 'input.hidden',
                                                          'fieldType': 'HiddenField',
                                                          'helpText': u'',
                                                          'jsRequired': None,
                                                          'label': None,
                                                          'name': 'siteMedia',
                                                          'required': None,
                                                          'type': 'hidden',
                                                          'value': '/static/media/'},
                                         'viewNameSource': {   'class': 'field',
                                                               'data-xp-type': 'input.hidden',
                                                               'fieldType': 'HiddenField',
                                                               'helpText': u'',
                                                               'jsRequired': None,
                                                               'label': None,
                                                               'name': 'viewNameSource',
                                                               'required': None,
                                                               'type': 'hidden',
                                                               'value': ''},
                                         'viewNameTarget': {   'class': 'field',
                                                               'data-xp-type': 'input.hidden',
                                                               'fieldType': 'HiddenField',
                                                               'helpText': u'',
                                                               'jsRequired': None,
                                                               'label': None,
                                                               'name': 'viewNameTarget',
                                                               'required': None,
                                                               'type': 'hidden',
                                                               'value': ' '}},
                        'isDefaultApp': False,
                        'isLogin': False,
                        'menus': {   'main': [],
                                     'service': [   {   'action': '',
                                                        'app': u'ximpia_site',
                                                        'appSlug': u'front',
                                                        'description': u'Home',
                                                        'icon': u'iconHome',
                                                        'image': '',
                                                        'isCurrent': True,
                                                        'isDefaultApp': True,
                                                        'items': [],
                                                        'name': u'home',
                                                        'params': {   },
                                                        'sep': False,
                                                        'service': u'Web',
                                                        'title': u'Home',
                                                        'view': u'home',
                                                        'viewSlug': u'home',
                                                        'winType': u'window',
                                                        'zone': u'service'}],
                                     'sys': [],
                                     'view': []},
                        'settings': {   u'NUMBER_RESULTS_LIST': 50,
                                        u'SIGNUP_SOCIAL_NETWORK': False,
                                        u'SIGNUP_USER_PASSWORD': True,
                                        u'SITE_SIGNUP_INVITATION': False},
                        'tmpl': {   u'home': u'home'},
                        'view': 'home',
                        'viewSlug': u'home',
                        'winType': u'window'},
        'status': 'OK'}