def r53_hosted_zone_id():
    """
    Return a mapping of (region, service) -> hosted zone id
    """
    input_map = {
        'ElasticBeanstalk': {
            'us-east-2':'Z14LCN19Q5QHIC',
            'us-east-1':'Z117KPS5GTRQ2G',
            'us-west-1':'Z1LQECGX5PH1X',
            'us-west-2':'Z38NKT9BP95V3O',
            'ap-south-1':'Z18NTBI3Y7N9TZ',
            'ap-northeast-3':'ZNE5GEY1TIAGY',
            'ap-northeast-2':'Z3JE5OI70TWKCP',
            'ap-southeast-1':'Z16FZ9L249IFLT',
            'ap-southeast-2':'Z2PCDNR3VC2G1N',
            'ap-northeast-1':'Z1R25G3KIG2GBW',
            'ca-central-1':'ZJFCZL7SSZB5I',
            'cn-north-1': 'None',
            'cn-northwest-1':'None',
            'eu-central-1':'Z1FRNW7UH4DEZJ',
            'eu-west-1':'Z2NYPWQ7DFZAZH',
            'eu-west-2':'Z1GKAAAUGATPF1',
            'eu-west-3':'Z5WN6GAYWG5OB',
            'eu-north-1':'Z23GO28BZ5AETM',
            'sa-east-1':'Z10X7K2B4QSOFV',
        },
        'ElasticLoadBalancing': {
            'us-east-2': 'Z3AADJGX6KTTL2',
            'us-east-1': 'Z35SXDOTRQ7X7K',
            'us-west-1': 'Z368ELLRRE2KJ0',
            'us-west-2': 'Z1H1FL5HABSF5',
            'ap-south-1': 'ZP97RAFLXTNZK',
            'ap-northeast-3': 'Z5LXEXXYW11ES',
            'ap-northeast-2': 'ZWKZPGTI48KDX',
            'ap-southeast-1': 'Z1LMS91P8CMLE5',
            'ap-southeast-2': 'Z1GM3OXH4ZPM65',
            'ap-northeast-1': 'Z14GRHDCWA56QT',
            'ca-central-1': 'ZQSVJUPU6J1EY',
            'cn-north-1': 'Z3BX2TMKNYI13Y',
            'cn-northwest-1': 'Z3BX2TMKNYI13Y',
            'eu-central-1': 'Z215JYRZR1TBD5',
            'eu-west-1': 'Z32O12XQLNTSW2',
            'eu-west-2': 'ZHURV8PSTC4K8',
            'eu-west-3': 'Z3Q77PNBQS71R4',
            'eu-north-1': 'Z23TAZ6LKFMNIO',
            'sa-east-1': 'Z2P70J7HTTTPLU',
        },
        'NetworkLoadBalancing': {
            'us-east-2': 'ZLMOA37VPKANP',
            'us-east-1': 'Z26RNL4JYFTOTI',
            'us-west-1': 'Z24FKFUX50B4VW',
            'us-west-2': 'Z18D5FSROUN65G',
            'ap-south-1': 'ZVDDRBQ08TROA',
            'ap-northeast-3': 'Z1GWIQ4HH19I5X',
            'ap-northeast-2': 'ZIBE1TIR4HY56',
            'ap-southeast-1': 'ZKVM4W9LS7TM',
            'ap-southeast-2': 'ZCT6FZBF4DROD',
            'ap-northeast-1': 'Z31USIVHYNEOWT',
            'ca-central-1': 'Z2EPGBW3API2WT',
            'cn-north-1': 'Z3QFB96KMJ7ED6',
            'cn-northwest-1': 'ZQEIKTCZ8352D',
            'eu-central-1': 'Z3F0SRJ5LGBH90',
            'eu-west-1': 'Z2IFOLAFXWLO4F',
            'eu-west-2': 'ZD4D7Y8KGAS4G',
            'eu-west-3': 'Z1CMS0P5QUZ6D5',
            'eu-north-1': 'Z1UDT6IFJ4EJM',
            'sa-east-1': 'ZTK26PT1VY4CU',
        },
        'CloudFront': {
            '_default': 'Z2FDTNDATAQYW2',  # Cloudfront has only one hosted zone id (global service)
        },
        'APIGateway': {
            'us-east-2': 'ZOJJZC49E0EPZ',
            'us-east-1': 'Z1UJRXOUMOOFQ8',
            'us-west-1': 'Z2MUQ32089INYE',
            'us-west-2': 'Z2OJLYMUO9EFXC',
            'ap-south-1': 'Z3VO1THU9YC4UR',
            'ap-northeast-3': 'Z2YQB5RD63NC85',
            'ap-northeast-2': 'Z20JF4UZKIW1U8',
            'ap-southeast-1': 'ZL327KTPIQFUL',
            'ap-southeast-2': 'Z2RPCDW04V8134',
            'ap-northeast-1': 'Z1YSHQZHG15GKL',
            'ca-central-1': 'Z19DQILCV0OWEC',
            'cn-north-1': 'None',
            'cn-northwest-1': 'None',
            'eu-central-1': 'Z1U9ULNL0V5AJ3',
            'eu-west-1': 'ZLY8HYME6SFDD',
            'eu-west-2': 'ZJ5UAJN8Y3Z2Q',
            'eu-west-3': 'Z3KY65QIEKYHQQ',
            'eu-north-1': 'Z2YB950C88HT6D',
            'sa-east-1': 'ZCMLWB8V5SYIT',
        },
    }

    # Aggregate all listed regions
    regions = set()
    for region_map in input_map.values():
        regions.update(region_map.keys())
    regions.discard('_default')

    output = {}
    for region in regions:
        for service in input_map:
            try:
                hosted_zone_id = input_map[service][region]
            except KeyError:
                hosted_zone_id = input_map[service]['_default']

            if region not in output:
                output[region] = {}
            output[region][service] = hosted_zone_id

    return output
