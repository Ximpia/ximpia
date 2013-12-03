Visual Conditions
=================

You can associate conditions to your visual objects so you control rendering and other visual behavior. When those conditions match or not, 
then your visual objects gain the property you associate with the condition.

Conditions are mapped in the view element ``id_view`` as attribute ``data-xp-cond-rules``:

.. code-block:: html

    <div    id="id_view" 
        data-xp="{viewName: 'signup'}" 
        data-xp-cond-rules="{   hasUserAuth: 'settings.SIGNUP_USER_PASSWORD == true', 
                                hasNetAuth: 'settings.SIGNUP_SOCIAL_NETWORK == true', 
                                hasNotNetAuth: 'settings.SIGNUP_SOCIAL_NETWORK == false',
                                showCaptcha: '  (   isSocialLogged == false && 
                                                    form_signup.invitationCode.value == \'\' && 
                                                        settings.SITE_SIGNUP_INVITATION == true     ) || 
                                                (   isSocialLogged == false && 
                                                        settings.SITE_SIGNUP_INVITATION == false     )',
                                requiresInvitation: 'settings.SITE_SIGNUP_INVITATION == true'
                            }" >
    </div>

In this case we compare to ``settings`` and ``isSocialLogged``. These variables would relate to the visual context. In case
you want to compare with a form field, you would do: ``form_myform.myfiel``. You may at your server-side write variables
to the visual context with ``self._add_attr('isSocialLogged', False)`` from service view.

Comparison Operators
--------------------

You can compare:

* ==
* !=
* >
* <
* >=
* <=

Logical Operators
-----------------

* OR : ``||``
* AND : ``&&``
 
You can include parenthesis ``(`` and ``)`` to provide right logic.


Visual Objects Conditions
-------------------------

After you define your view conditions, it is time to map those conditions to your objects.

Our current release forces you to include ``container`` visual object, where you place condition logic. In future releases,
we will have condition support in all objects.

.. code-block:: html

    <div id="id_socialAuth" style="margin-top: 5px;" 
        data-xp-type="container" 
        data-xp-cond="{conditions: [ 
                                        {condition: 'hasNetAuth', action: 'render', value: true}
                                    ]}" >
    <div id="id_facebookSignup_comp" 
            data-xp-type="function.render" 
            data-xp="{functionName: 'ximpia.external.Facebook.renderSignup'}" > </div>
        <div class="caption"><span>You can also:</span><br/></div>
        <!-- Facebook Signup Button -->
        <div class="fb-login-button" 
                data-show-faces="true" 
                data-width="200" 
                data-max-rows="1" 
                scope="email">Signup with Facebook</div>
    </div>
    </div>

When condition ``hasNetAuth`` matches we render facebook login component. When not, we do not render facebook login.

You can include a set of conditions to match. The first to match, we apply action and skip the rest. The only action currently
supported os ``render``, where you can place to ``true`` to show or ``false`` to hide.

