class PayPalParamsTemplate(object):
    """
    Mapping from Classic API fields to REST API JSON structure.

    Classic API docs:
        developer.paypal.com/webapps/developer/docs/classic/api/merchant/SetExpressCheckout_API_Operation_NVP/
        developer.paypal.com/webapps/developer/docs/classic/api/merchant/GetExpressCheckoutDetails_API_Operation_NVP/
        developer.paypal.com/webapps/developer/docs/classic/api/merchant/DoExpressCheckoutPayment_API_Operation_NVP/
    """

    template = {
        'intent': 'PAYMENTREQUEST_0_PAYMENTACTION',  # Sale | Authorization | Order
        'payer': {
            'payer_info': {
                'email': 'EMAIL',
                'shipping_address': {
                    'recipient_name': 'PAYMENTREQUEST_0_SHIPTONAME',
                    'line1': 'PAYMENTREQUEST_0_SHIPTOSTREET',
                    'line2': 'PAYMENTREQUEST_0_SHIPTOSTREET2',
                    'city': 'PAYMENTREQUEST_0_SHIPTOCITY',
                    'country_code': 'PAYMENTREQUEST_0_SHIPTOCOUNTRYCODE',
                    'country_name': 'PAYMENTREQUEST_0_SHIPTOCOUNTRYNAME',  # Response (Classic GET)
                    'postal_code': 'PAYMENTREQUEST_0_SHIPTOZIP',
                    'state': 'PAYMENTREQUEST_0_SHIPTOSTATE',
                    'phone': 'PAYMENTREQUEST_0_SHIPTOPHONENUM',
                    'status': 'PAYMENTREQUEST_0_ADDRESSSTATUS',  # Response (Classic GET)
                    'normalization_status': 'PAYMENTREQUEST_0_ADDRESSNORMALIZATIONSTATUS',  # Response (Classic GET)
                },

                # Response:
                'first_name': 'FIRSTNAME',
                'last_name': 'LASTNAME',
                'payer_id': 'PAYERID',
                'phone': 'PHONENUM',

                # Response (Classic GET)
                'middle_name': 'MIDDLENAME',
                'status': 'PAYERSTATUS',  # verified | unverified
                'suffix': 'SUFFIX',
                'business': 'BUSINESS',
                'country_code': 'COUNTRYCODE',
            },

            # Classic:
            'require_confirmed_shipping_address': 'REQCONFIRMSHIPPING',
            'override_shipping_address': 'ADDROVERRIDE',
        },
        'transactions': [
            {
                'description': 'PAYMENTREQUEST_{}_DESC',
                'item_list': {
                    'items': [
                        {
                            'name': 'L_PAYMENTREQUEST_{}_NAME{}',
                            'sku': 'L_PAYMENTREQUEST_{}_NUMBER{}',
                            'price': 'L_PAYMENTREQUEST_{}_AMT{}',
                            'currency': 'PAYMENTREQUEST_{}_CURRENCYCODE',  # NOTE: Classic API transaction currency
                            'quantity': 'L_PAYMENTREQUEST_{}_QTY{}',

                            # Classic:
                            'description': 'L_PAYMENTREQUEST_{}_DESC{}',
                            'tax': 'L_PAYMENTREQUEST_{}_TAXAMT{}',
                            'url': 'L_PAYMENTREQUEST_{}_ITEMURL{}',
                            'category': 'L_PAYMENTREQUEST_{}_ITEMCATEGORY{}',  # Digital | Physical
                            'weight': {
                                'value': 'L_PAYMENTREQUEST_{}_ITEMWEIGHTVALUE{}',
                                'unit': 'L_PAYMENTREQUEST_{}_ITEMWEIGHTUNIT{}',
                            },
                            'length': {
                                'value': 'L_PAYMENTREQUEST_{}_ITEMLENGTHVALUE{}',
                                'unit': 'L_PAYMENTREQUEST_{}_ITEMLENGTHUNIT{}',
                            },
                            'width': {
                                'value': 'L_PAYMENTREQUEST_{}_ITEMWIDTHVALUE{}',
                                'unit': 'L_PAYMENTREQUEST_{}_ITEMWIDTHUNIT{}',
                            },
                            'height': {
                                'value': 'L_PAYMENTREQUEST_{}_ITEMHEIGHTVALUE{}',
                                'unit': 'L_PAYMENTREQUEST_{}_ITEMHEIGHTUNIT{}',
                            },
                        }
                    ],

                    # Classic:
                    'auctions': [
                        {
                            'item': 'L_PAYMENTREQUEST_{}_EBAYITEMNUMBER{}',
                            'transaction': 'L_PAYMENTREQUEST_{}_EBAYITEMAUCTIONTXNID{}',
                            'order': 'L_PAYMENTREQUEST_{}_EBAYITEMORDERIDm',
                            'cart': 'L_PAYMENTREQUEST_{}_EBAYCARTID{}',
                        }
                    ],
                },

                'amount': {
                    'total': 'PAYMENTREQUEST_{}_AMT',
                    'currency': 'PAYMENTREQUEST_{}_CURRENCYCODE',
                    'details': {
                        'subtotal': 'PAYMENTREQUEST_{}_ITEMAMT',
                        'tax': 'PAYMENTREQUEST_{}_TAXAMT',
                        'shipping': 'PAYMENTREQUEST_{}_SHIPPINGAMT',

                        # Classic:
                        'shipping_discount': 'PAYMENTREQUEST_{}_SHIPDISCAMT',
                        'handling': 'PAYMENTREQUEST_{}_HANDLINGAMT',
                    },
                },

                # Classic:
                'tracking': {
                    'invoice': 'PAYMENTREQUEST_{}_INVNUM',
                    'transaction': 'PAYMENTREQUEST_{}_TRANSACTIONID',
                    'payment': 'PAYMENTREQUEST_{}_PAYMENTREQUESTID',
                    'custom': 'PAYMENTREQUEST_{}_CUSTOM',
                },
                'insurance': {
                    'offered': 'PAYMENTREQUEST_{}_INSURANCEOPTIONOFFERED',
                    'amount': 'PAYMENTREQUEST_{}_INSURANCEAMT',
                    'selected': 'INSURANCEOPTIONSELECTED',  # Response (Classic GET)

                },
                'ipn_url': 'PAYMENTREQUEST_{}_NOTIFYURL',
                'payment_reason': 'PAYMENTREQUEST_{}_PAYMENTREASON',
                'multi_shipping': 'PAYMENTREQUEST_{}_MULTISHIPPING',
                'note': 'PAYMENTREQUEST_{}_NOTETEXT',
                'payment_method': 'PAYMENTREQUEST_{}_ALLOWEDPAYMENTMETHOD',
                'category': 'PAYMENTREQUEST_{}_BUCKETCATEGORYTYPE',  # 1 (international shipping) | 2 (local delivery)
                'seller_id': 'PAYMENTREQUEST_{}_SELLERPAYPALACCOUNTID',
            }
        ],

        'redirect_urls': {
            'return_url': 'RETURNURL',
            'cancel_url': 'CANCELURL',
        },

        # Classic:
        'page': {
            'locale': 'LOCALECODE',
            'flow': 'SOLUTIONTYPE',  # Sole | Mark (buyer needs paypal)
            'prompt': 'LANDINGPAGE',  # Billing | Login
            'shipping_address': 'NOSHIPPING',
            'layout': {
                'template': 'PAGESTYLE',
                'brand': 'BRANDNAME',
                'logo': 'LOGOIMG',
                'cart_color': 'CARTBORDERCOLOR',
                'header': 'HDRIMG',
                'background_color': 'PAYFLOWCOLOR',
                'total_label': 'TOTALTYPE',
            },
        },
        'shipping_options': {
            'options': [
                {
                    'default': 'L_SHIPPINGOPTIONISDEFAULT{}',
                    'name': 'L_SHIPPINGOPTIONNAME{}',
                    'amount': 'L_SHIPPINGOPTIONAMOUNT{}',
                }
            ],
            'selected': {  # Response (Classic GET)
                'calculation': 'SHIPPINGCALCULATIONMODE',
                'is_default': 'SHIPPINGOPTIONISDEFAULT',
                'name': 'SHIPPINGOPTIONNAME',
                'amount': 'SHIPPINGOPTIONAMOUNT',
            }
        },
        'max_amount': 'MAXAMT',
        'allow_note': 'ALLOWNOTE',
        'channel': 'CHANNELTYPE',
        'callback': {
            'url': 'CALLBACK',
            'timeout': 'CALLBACKTIMEOUT',
            'version': 'CALLBACKVERSION'
        },
        'funding': {
            'allow': 'ALLOWPUSHFUNDING',
            'source': 'USERSELECTEDFUNDINGSOURCE',
        },
        'customer_service_number': 'CUSTOMERSERVICENUMBER',
        'gift': {
            'message': 'GIFTMESSAGE',  # Response (Classic GET)
            'message_enabled': 'GIFTMESSAGEENABLE',
            'receipt_enabled': 'GIFTRECEIPTENABLE',
            'wrapping': {
                'enabled': 'GIFTWRAPENABLE',
                'label': 'GIFTWRAPNAME',
                'amount': 'GIFTWRAPAMOUNT',
            }
        },
        'newsletter_enable': 'BUYEREMAILOPTINENABLE',
        'survey': {
            'enabled': 'SURVEYENABLE',
            'question': 'SURVEYQUESTION',
            'answer_list': {
                'selected': 'SURVEYCHOICESELECTED',  # Response (Classic GET)
                'answers': [
                    {
                        'text': 'L_SURVEYCHOICE{}'
                    }
                ],
            }
        },
        'buyer': {
            'id': 'BUYERID',
            'username': 'BUYERUSERNAME',
            'email': 'BUYERMARKETINGEMAIL',  # Response (Classic GET)
            'registration_date': 'BUYERREGISTRATIONDATE',
        },
        'giro_payment': {
            'success_url': 'GIROPAYSUCCESSURL',
            'cancel_url': 'GIROPAYCANCELURL',
        },
        'bank_transfer': {
            'pending_url': 'BANKTXNPENDINGURL',
        },
        'billing_agreements': [
            {
                'type': 'L_BILLINGTYPE{}',
                'description': 'L_BILLINGAGREEMENTDESCRIPTION{}',
                'payment': 'L_PAYMENTTYPE{}',
                'custom': 'L_BILLINGAGREEMENTCUSTOM{}',
            }
        ],
        'tax_id_type': 'TAXIDTYPE',
        'tax_id': 'TAXID',

        # Response
        'id': 'TOKEN',
        'create_time': 'TIMESTAMP',

        # Response (Classic GET):
        'status': 'ACK',
        'state': 'CHECKOUTSTATUS',  # PaymentActionNotInitiated | ..Failed | ..InProgress | ..Completed
        'correlation_id': 'CORRELATIONID',
        'build': 'BUILD',
        'version': 'VERSION',
        'note': 'NOTE',
        'paypal_adjustment': 'PAYPALADJUSTMENT',
        'redirect_required': 'REDIRECTREQUIRED',
        'payment_errors': [
            {
                'name': 'PAYMENTINFO_{}_SHORTMESSAGE',
                'message': 'PAYMENTINFO_{}_LONGMESSAGE',
                'error_code': 'PAYMENTINFO_{}_ERRORCODE',
                'severity_code': 'PAYMENTINFO_{}_SEVERITYCODE',
                'ack': 'PAYMENTINFO_{}_ACK',
            }
        ],
        'errors': [
            {
                'name': 'L_SHORTMESSAGE{}',
                'message': 'L_LONGMESSAGE{}',
                'error_code': 'L_ERRORCODE{}',
                'severity_code': 'L_SEVERITYCODE{}',
            }
        ]

     #u'PAYMENTINFO_0_ACK': u'Success',
     #u'PAYMENTINFO_0_AMT': u'4385.00',
     #u'PAYMENTINFO_0_CURRENCYCODE': u'SEK',
     #u'PAYMENTINFO_0_ERRORCODE': u'0',
     #u'PAYMENTINFO_0_FEEAMT': u'174.27',
     #u'PAYMENTINFO_0_ORDERTIME': u'2014-02-04T23:04:48Z',
     #u'PAYMENTINFO_0_PAYMENTSTATUS': u'Completed',
     #u'PAYMENTINFO_0_PAYMENTTYPE': u'instant',
     #u'PAYMENTINFO_0_PENDINGREASON': u'None',
     #u'PAYMENTINFO_0_PROTECTIONELIGIBILITY': u'PartiallyEligible',
     #u'PAYMENTINFO_0_PROTECTIONELIGIBILITYTYPE': u'ItemNotReceivedEligible',
     #u'PAYMENTINFO_0_REASONCODE': u'None',
     #u'PAYMENTINFO_0_RECEIPTID': u'4616-4165-4298-1473',
     #u'PAYMENTINFO_0_SECUREMERCHANTACCOUNTID': u'DC5YMCCERWPUE',
     #u'PAYMENTINFO_0_TAXAMT': u'0.00',
     #u'PAYMENTINFO_0_TRANSACTIONID': u'8XF34547TK509205D',
     #u'PAYMENTINFO_0_TRANSACTIONTYPE': u'cart',
    }
